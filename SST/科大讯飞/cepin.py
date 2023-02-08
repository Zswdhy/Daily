#!/usr/bin/python
# -*- coding: UTF-8 -*-
import base64
import hashlib
import json
import time
import requests


def audio_score(path, text):
    """
    获取音频得分
    :param path:音频地址
    :param text:音频对应文本
    :return:
    """
    x_appid = '5d461a04'
    api_key = '359e88beaff821f51ff1ac0346b20e5d'
    curTime = str(int(time.time()))
    url = 'http://api.xfyun.cn/v1/service/v1/ise'

    with open(path, 'rb') as f:
        file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = {'audio': base64_audio, 'text': text}
    param = json.dumps({"aue": "raw", "result_level": "entirety", "language": "en_us", "category": "read_sentence", })
    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    m2 = hashlib.md5()
    m2.update((api_key + curTime + paramBase64).encode('utf-8'))
    checkSum = m2.hexdigest()
    x_header = {
        'X-Appid': x_appid,
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    req = requests.post(url, data=body, headers=x_header)
    result = json.loads(req.content.decode('utf-8'))
    score = round(float(result['data']['read_sentence']['rec_paper']['read_chapter']['total_score']) / 10 * 7 / 10, 2)
    print('该波段语音语调综合得分', score)

    return score


if __name__ == '__main__':
    path = "../static/d.wav"
    text = "A child's education has never been about learning Information and basic skills only it has always included teaching the next generation how to be good members of society. Therefore, this cannot be the responsibility of the parents alone. In order to be a good member of any society, the individual must respect and obey the rules of their community and share their values."

    a = audio_score(path, text)
