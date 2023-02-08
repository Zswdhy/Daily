import base64
import hashlib
import hmac
import os
import time
import json

import requests

from pydub import AudioSegment
from pydub.silence import split_on_silence

lfasr_host = 'http://raasr.xfyun.cn/api'

# 请求的接口名
api_prepare = '/prepare'
api_upload = '/upload'
api_merge = '/merge'
api_get_progress = '/getProgress'
api_get_result = '/getResult'
# 文件分片大小10M
file_piece_sice = 10485760

# ——————————————————转写可配置参数————————————————
# 参数可在官网界面（https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E8%BD%AC%E5%86%99.html）查看，根据需求可自行在gene_params方法里添加修改
# 转写类型
lfasr_type = 0
# 是否开启分词
has_participle = 'false'
has_seperate = 'true'
# 多候选词个数
max_alternatives = 0
# 子用户标识
suid = ''


class SliceIdGenerator:
    """slice id生成器"""

    def __init__(self):
        self.__ch = 'aaaaaaaaa`'

    def getNextSliceId(self):
        ch = self.__ch
        j = len(ch) - 1
        while j >= 0:
            cj = ch[j]
            if cj != 'z':
                ch = ch[:j] + chr(ord(cj) + 1) + ch[j + 1:]
                break
            else:
                ch = ch[:j] + 'a' + ch[j + 1:]
                j = j - 1
        self.__ch = ch
        return self.__ch


class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path, to_file):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.to_file = to_file

    # 根据不同的apiname生成不同的参数,本示例中未使用全部参数您可在官网(https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E8%BD%AC%E5%86%99.html)查看后选择适合业务场景的进行更换
    def gene_params(self, apiname, taskid=None, slice_id=None):
        appid = self.appid
        secret_key = self.secret_key
        upload_file_path = self.upload_file_path
        ts = str(int(time.time()))
        m2 = hashlib.md5()
        m2.update((appid + ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)
        param_dict = {'app_id': appid, 'signa': signa, 'ts': ts, 'has_participle': "true", "eng_vad_margin": 0,
                      "has_smooth": "true"}

        if apiname == api_prepare:
            # slice_num是指分片数量，如果您使用的音频都是较短音频也可以不分片，直接将slice_num指定为1即可
            slice_num = int(file_len / file_piece_sice) + (0 if (file_len % file_piece_sice == 0) else 1)
            param_dict['file_len'] = str(file_len)
            param_dict['file_name'] = file_name
            param_dict['slice_num'] = str(slice_num)
        elif apiname == api_upload:
            param_dict['task_id'] = taskid
            param_dict['slice_id'] = slice_id
        elif apiname == api_merge:
            param_dict['task_id'] = taskid
            param_dict['file_name'] = file_name
        elif apiname == api_get_progress or apiname == api_get_result:
            param_dict['task_id'] = taskid
        return param_dict

    # 请求和结果解析，结果中各个字段的含义可参考：https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E8%BD%AC%E5%86%99.html
    def gene_request(self, apiname, data, files=None, headers=None):
        response = requests.post(lfasr_host + apiname, data=data, files=files, headers=headers)
        result = json.loads(response.text)
        if result["ok"] == 0:
            # print("{} success:".format(apiname) + str(result))
            return result
        else:
            # print("aa  {} error:".format(apiname) + str(result))
            return result

    # 预处理
    def prepare_request(self):
        return self.gene_request(apiname=api_prepare,
                                 data=self.gene_params(api_prepare))

    # 上传
    def upload_request(self, taskid, upload_file_path):
        file_object = open(upload_file_path, 'rb')
        try:
            index = 1
            sig = SliceIdGenerator()
            while True:
                content = file_object.read(file_piece_sice)
                if not content or len(content) == 0:
                    break
                files = {
                    "filename": self.gene_params(api_upload).get("slice_id"),
                    "content": content
                }
                response = self.gene_request(api_upload,
                                             data=self.gene_params(api_upload,
                                                                   taskid=taskid,
                                                                   slice_id=sig.getNextSliceId()),
                                             files=files)
                if response.get('ok') != 0:
                    # 上传分片失败
                    # print('upload slice fail, response: ' + str(response))
                    return False
                # print('upload slice ' + str(index) + ' success')
                index += 1
        finally:
            'file index:' + str(file_object.tell())
            file_object.close()
        return True

    # 合并
    def merge_request(self, taskid):
        return self.gene_request(api_merge, data=self.gene_params(api_merge, taskid=taskid))

    # 获取进度
    def get_progress_request(self, taskid):
        return self.gene_request(api_get_progress, data=self.gene_params(api_get_progress, taskid=taskid))

    # 获取结果
    def get_result_request(self, taskid):
        return self.gene_request(api_get_result, data=self.gene_params(api_get_result, taskid=taskid))

    def all_api_request(self):
        # 1. 预处理
        pre_result = self.prepare_request()
        taskid = pre_result["data"]
        # 2 . 分片上传
        self.upload_request(taskid=taskid, upload_file_path=self.upload_file_path)
        # 3 . 文件合并
        self.merge_request(taskid=taskid)
        # 4 . 获取任务进度
        while True:
            # 每隔20秒获取一次任务进度
            progress = self.get_progress_request(taskid)
            progress_dic = progress
            if progress_dic['err_no'] != 0 and progress_dic['err_no'] != 26605:
                # print('task error: ' + progress_dic['failed'])
                return None, progress_dic['failed']
            else:
                data = progress_dic['data']
                task_status = json.loads(data)
                if task_status['status'] == 9:
                    # print('task ' + taskid + ' finished')
                    break
                # print('The task ' + taskid + ' is in processing, task status: ' + str(data))

            # 每次获取进度间隔20S
            time.sleep(1)
        # 5 . 获取结果
        res = self.get_result_request(taskid=taskid)
        r = json.loads(res["data"])
        text = ""
        for iterating_var in r:
            text += iterating_var["onebest"]
        return text, "转换成功"


def fun_TTS(kind, text, sex):
    """
    文本转语音
    :param kind:
    :param text: 输入的文本，可以是中文或者英文
    :param sex: 输入的性别，支持男女声
    :return:
    """

    import pyttsx3

    t = time.time()
    t = int(t)
    engine = pyttsx3.init()

    txt = text
    a = sex
    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[a].id)  # 调整人声类型

    rate = engine.getProperty('rate')

    engine.setProperty('rate', 150)  # 调整语速,范围一般在0~500之间

    volume = engine.getProperty('volume')

    engine.setProperty('volume', 0.8)  # 调整声量，范围在0~1之间

    engine.say('语音合成开始')

    engine.runAndWait()

    # 保存音频到本地，格式为wav
    engine.save_to_file(txt, 'static/' + "res_" + str(t) + '.wav')

    engine.runAndWait()
    print("执行完毕")

    _urlname_ = str(t) + '.wav'
    return _urlname_


def audio_chunk():
    """
    音频切分
    :return:
    """

    """
    channels:音频通道
    frame_rate:音频比率【采样率】
    sample_width:样本字节数【数据位宽】
    max:最大振幅
    len(sound):时长（毫秒）
    raw_data：字节数据

    normalize(sound)  :使音量正常化
    """

    path = "static/2黄成龙-202141.wav"
    name = path.split("/")[-1].split(".")[0]

    sound = AudioSegment.from_mp3(path)
    print("path_1.sound", "channels", sound.channels, "frame_rate", sound.frame_rate, "sample_width",
          sound.sample_width, "max", sound.max, "time", len(sound))

    chunks = split_on_silence(
        sound,
        min_silence_len=460,
        silence_thresh=-45,
        keep_silence=400
    )
    print('总分段：', len(chunks))
    for i in list(range(len(chunks)))[::-1]:
        if len(chunks[i]) <= 1000 or len(chunks[i]) >= 10000:
            chunks.pop(i)
    print('取有效分段(大于2s小于10s)：', len(chunks))

    for i, chunk in enumerate(chunks):
        file_name = f"./static/{name}_chunk{i}.wav"
        chunk.export(file_name, format="wav")


if __name__ == '__main__':
    path = "./static/d.wav"
    api = RequestApi(
        appid="9cfa8007",
        secret_key="dac155f99cc6889677bc85d3b3b12496",
        upload_file_path=str(path),
        to_file=str(path)
    )
    data, msg = api.all_api_request()
    print("data", data, "type", type(data))
    print("msg", msg, "type", type(msg))

    content = "A child's education has never been about learning Information and basic skills only it has always included teaching the next generation how to be good members of society. Therefore, this cannot be the responsibility of the parents alone. In order to be a good member of any society, the individual must respect and obey the rules of their community and share their values."
    fun_TTS(kind=0, text=content, sex=1)

    audio_chunk()
