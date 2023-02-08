import websocket
import datetime
import hashlib
import base64
import hmac
import json

import sys
from urllib.parse import urlencode
import logging
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import re


# from textblob import TextBlob as tb
def text_punt_blank(strings):
    def is_chinese(string):
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def sentence_split(text):
        """
        将一个段落分成若干句子，以分号，句号作为切分。
        """
        # text = remove_space(text)

        start = 0
        result = []
        # result = re.split(r'(\.|\!|\?|。|！|？|\.{6})', text)
        groups = re.finditer('\.|\?|\!', text)

        for i in groups:
            end = i.span()[1]
            result.append(text[start:end])
            start = end
        # last one
        result.append(text[start:])
        for i in result:
            if i == '':
                result.remove('')
        return result

    # f=open('testt.txt',encoding='utf-8').read()
    flist = sentence_split(strings)
    print('dd', flist)
    sentence = [str(i).split(' ') for i in flist]
    print('sentence', sentence)
    for i in sentence:
        while '' in i:
            i.remove('')
            pass
        for j in i:
            if is_chinese(j):
                i.remove(j)
    new_sentenc = [' '.join(i) for i in sentence]
    new_sentenc = ' '.join(new_sentenc).replace(' ,', ',').replace(' .', '.').replace(' , ,', ',').replace(' ， ，', ',')
    return new_sentenc


def main(path1):
    res = []
    type = sys.getfilesystemencoding()

    try:
        import thread
    except ImportError:
        import _thread as thread

    logging.basicConfig()

    STATUS_FIRST_FRAME = 0  # 第一帧的标识
    STATUS_CONTINUE_FRAME = 1  # 中间帧标识
    STATUS_LAST_FRAME = 2  # 最后一帧的标识

    global wsParam

    class Ws_Param(object):
        # 初始化
        def __init__(self, host, APPID, wav):
            self.Host = host
            self.HttpProto = "HTTP/1.1"
            self.HttpMethod = "GET"
            self.RequestUri = "/v2/iat"
            self.APPID = APPID
            self.Algorithm = "hmac-sha256"
            self.url = "wss://" + self.Host + self.RequestUri

            # 设置测试音频文件，流式听写一次最多支持60s，超过60s会引起超时等错误。
            self.wav = path1
            self.CommonArgs = {"app_id": self.APPID}
            self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", 'vinfo': 1}

        def create_url(self, APIKey, APISecret):
            url = 'wss://ws-api.xfyun.cn/v2/iat'
            now = datetime.now()
            date = format_date_time(mktime(now.timetuple()))
            signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
            signature_origin += "date: " + date + "\n"
            signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
            signature_sha = hmac.new(APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                     digestmod=hashlib.sha256).digest()
            signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

            authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
                APIKey, "hmac-sha256", "host date request-line", signature_sha)
            authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
            v = {
                "authorization": authorization,
                "date": date,
                "host": "ws-api.xfyun.cn"
            }
            url = url + '?' + urlencode(v)
            return url

    # 收到websocket消息的处理
    def on_message(ws, message):
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                errMsg = json.loads(message)["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                print(message)
                data = [i['cw'][0]['w'] for i in json.loads(message)["data"]['result']['ws']]
                haah = json.dumps(data, ensure_ascii=False)
                res.append(json.loads(haah))
                # [i['cw'] for i in data]
                print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
                return json.dumps(data, ensure_ascii=False)
        except Exception as e:
            print("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def on_error(ws, error):
        print("### error:", error)

    # 收到websocket关闭的处理
    def on_close(ws):
        # print(ws.on_message)
        print("### closed ###")

    # 收到websocket连接建立的处理
    def on_open(ws):
        def run(*args):
            # frameSize = 1280  # 每一帧的音频大小
            frameSize = 5120  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            while True:
                buf = path1.read(frameSize)

                # 文件结束
                if not buf:
                    status = STATUS_LAST_FRAME
                # 第一帧处理
                # 发送第一帧音频，带business 参数
                # appid 必须带上，只需第一帧发送
                if status == STATUS_FIRST_FRAME:

                    d = {"common": wsParam.CommonArgs,
                         "business": wsParam.BusinessArgs,
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    d = json.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                    time.sleep(1)
                    break
                # 模拟音频采样间隔
                time.sleep(intervel)
            ws.close()

        # run()
        thread.start_new_thread(run, ())

    wsParam = Ws_Param("ws-api.xfyun.cn",
                       APPID='5d461a04',
                       wav=path1,
                       )
    # websocket.enableTrace(False)
    # TODO: 在控制台-我的应用-语音听写（流式版）获取APIKey和APISecret
    wsUrl = wsParam.create_url(APIKey='8074997f2287ab7e46acfc92f40deea1',
                               APISecret='e01424bbb47be47ccd8af47190a0a2b7')
    print("wsUrl", wsUrl)
    print("-" * 100)
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    # # print(ws.recv())
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    res = ' '.join([' '.join(i) for i in res])
    new_Res = text_punt_blank(res)
    return new_Res


if __name__ == '__main__':
    text = "A child's education has never been about learning Information and basic skills only it has always included teaching the next generation how to be good members of society. Therefore, this cannot be the responsibility of the parents alone. In order to be a good member of any society, the individual must respect and obey the rules of their community and share their values."
    a = text_punt_blank(text)
    print("a", a)
    path = "../static/d.wav"
    b = main(path)
    print("b", b)
