from aip import AipSpeech  # pip install baidu-aip


def str_to_sound(txt, name):
    APP_ID = '11645517'
    API_KEY = 'fjKDHHHVin9dFlG8Vzq6zXnX'
    SECRET_KEY = 'hs3kAGTlwKLmpPLWR125Ly3knSj6eFTl'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    a = txt
    result = client.synthesis(a, 'zh', 1, {'spd': 5, 'vol': 6, 'per': 2})

    if not isinstance(result, dict):
        with open("../static/%s.mp3" % name, 'wb') as f:
            f.write(result)


if __name__ == '__main__':
    name = "baidu_sst"
    txt = "A child's education has never been about learning Information and basic skills only it has always included teaching the next generation how to be good members of society. Therefore, this cannot be the responsibility of the parents alone. In order to be a good member of any society, the individual must respect and obey the rules of their community and share their values."

    str_to_sound(txt, name)
