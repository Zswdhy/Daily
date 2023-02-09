import re
import time

import pandas as pd
import requests
from lxml import etree


def get_verb_word_pos(res):
    """
    有道翻译第一词性原则
    名词 ---> 名词复数
    动词【单性/多性】 ---> vbz、vbd、vbn、vbg、及物不及物标签
    形容词、副词、介词

    :return:
    """

    single_verb = []
    plus_verb = []
    noun_verb = []
    non_verb = []

    for index, item in enumerate(res):
        word = item

        url = f"https://dict.youdao.com/search?q={word}&keyfrom=new-fanyi.smartResult"
        time.sleep(1)
        try:
            _html = requests.get(url)
            html = etree.HTML(_html.content)
            pos_ = html.cssselect('div.clearfix div.trans-container li')
            temp = []

            # 获取词性
            for item in pos_:
                if str(item.text)[0].isalpha():
                    temp.append(str(item.text).split('.')[0])
            # vbz、vbg、vbd、vbn
            verb_style = html.cssselect('div.clearfix p.additional')
            verb_from = [''] * 4
            if verb_style:
                for item in verb_style:
                    _res = item.text.replace('[', "").replace(']', '').split()
                    for i in range(len(_res)):
                        if _res[i] == "第三人称单数":
                            verb_from[0] = _res[i + 1]
                            i += 2
                        elif _res[i] == "现在分词":
                            verb_from[1] = _res[i + 1]
                            i += 2
                        elif _res[i] == "过去式":
                            verb_from[2] = _res[i + 1]
                            i += 2
                        elif _res[i] == "过去分词":
                            verb_from[3] = _res[i + 1]
                            i += 2
                        else:
                            i += 1

            pos = ""
            if "及物动词" in html:
                if "不及物动词" in html:
                    pos = 'vt. & vi.'
                else:
                    pos = 'vt.'
            elif "不及物动词" in html:
                pos = 'vi.'

            if 'v' in temp:
                if len(temp) > 1:
                    # 多词性
                    plus_verb.append([word, pos, "、".join(temp)] + verb_from)
                elif len(temp) == 1:
                    # 单次性
                    single_verb.append([word, pos] + verb_from)

            if not temp:
                continue

            first_temp = temp[0]
            if first_temp in ["adv", "adj", "prep"]:
                non_verb.append([word, first_temp])
            elif first_temp == "n":
                plural = re.search(r"复数\s+(\w+)", _html.text)
                if plural:
                    noun_verb.append([word, plural.group(1)])
            print('\033[0;32;40msuccess：\033[0m', index + 1, word, )
        except Exception as e:
            with open("error.csv", "a") as file:
                file.write(word + "--->" + str(e) + "\n")
                file.close()
            print('\033[0;31;40mfail：\033[0m', index + 1, word, e)

    df1 = pd.DataFrame(single_verb, columns=['word', 'pos', 'vbz', 'vbg', 'vbd', 'vbn'])
    df2 = pd.DataFrame(plus_verb, columns=['word', 'pos', 'pos_', 'vbz', 'vbg', 'vbd', 'vbn'])
    df3 = pd.DataFrame(noun_verb, columns=['word', 'plural'])
    df4 = pd.DataFrame(non_verb, columns=['word', 'pos'])

    df1.to_csv('new_single_verb.csv', encoding='utf-8', index=False)
    df2.to_csv('new_plus_verb.csv', encoding='utf-8', index=False)
    df3.to_csv('new_noun.csv', encoding='utf-8', index=False)
    df4.to_csv('new_non_verb.csv', encoding='utf-8', index=False)


if __name__ == '__main__':
    res = ["apple"]
    get_verb_word_pos(res)
