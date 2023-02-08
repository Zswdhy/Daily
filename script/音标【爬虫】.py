import re
import time

import numpy as np
import pandas
import requests


def get_verb_word_pos():
    """
    获取动词的词性 vt. 和 vi.
    :return:
    """
    df = pandas.read_csv("words.csv", skiprows=0)
    res = np.array(df).tolist()[64001:]
    final = []
    for index, item in enumerate(res):
        word = item[0]
        print(index + 1, word)

        url = f"https://dict.youdao.com/search?q={word}&keyfrom=new-fanyi.smartResult"
        time.sleep(1)
        try:
            res = requests.get(url)
            html = res.content.decode("utf8")
            _temp = [word]
            if "及物动词" in html:
                if "不及物动词" in html:
                    _temp.append('vt. & vi.')
                else:
                    _temp.append('vt.')
            elif "不及物动词" in html:
                _temp.append('vi.')
            else:
                continue
            rule_4 = "第三人称单数\s+(\w+)\s"  #
            rule_5 = "现在分词\s+(\w+)\s"
            rule_6 = "过去式\s+(\w+)\s"
            rule_7 = "过去分词\s+(\w+)\s"

            if re.findall(rule_4, html):
                _temp.append(re.findall(rule_4, html)[0])
            else:
                _temp.append("")

            if re.findall(rule_5, html):
                _temp.append(re.findall(rule_5, html)[0])
            else:
                _temp.append("")

            if re.findall(rule_6, html):
                _temp.append(re.findall(rule_6, html)[0])
            else:
                _temp.append("")

            if re.findall(rule_7, html):
                _temp.append(re.findall(rule_7, html)[0])
            else:
                _temp.append("")
            final.append(_temp)
        except Exception as e:
            with open("error64001.csv", "a") as file:
                file.write(word + "\n")
                file.close()

    df_1 = pandas.DataFrame(final, columns=["word", 'pos', "vbz", "vbg", "vbd", "vbn"])

    df_1.to_csv("result64001.csv", encoding="utf-8", index=False)


if __name__ == '__main__':
    get_verb_word_pos()
