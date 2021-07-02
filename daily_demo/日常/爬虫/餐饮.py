import requests
import time

url = "https://sh.58.com/zplvyoujiudian/?utm_source=market&spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT&PGTID=0d202408-0000-2aa1-20c2-500c20126847&ClickID=2"
headers = {
    # ":authority": "sh.58.com",
    # ":method": "GET",
    # ":path": "/zplvyoujiudian/?utm_source=market&spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT&PGTID=0d202408-0000-2aa1-20c2-500c20126847&ClickID=2",
    # ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "time_create=1608988369863; userid360_xml=7838BBA669BEDEDF3CB686901B6193D6; f=n; commontopbar_new_city_info=2%7C%E4%B8%8A%E6%B5%B7%7Csh; id58=c5/nn10/3Kg2iVvBwOuyAg==; city=sh; 58home=sh; 58tj_uuid=98bee472-a623-4af3-ab9a-0089e916c735; als=0; wmda_uuid=78781c6394ff9d7dc86e703135948fd8; wmda_new_uuid=1; xxzl_deviceid=Wi%2BQCiTUjJJA1FVO7qMDU1g0EbasQEdsQWbfY7z9vB6dEU2SCU8yRDpaEURbZ1K4; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1606396424; ppStore_fingerprint=7A295B51A124C9E81F1C0F735B3B32D539C5CF84B9C82CA5%EF%BC%BF1606396423689; gr_user_id=1dce4169-5ad9-4ab6-9a72-b8aa36439760; __utma=253535702.1529028131.1606396445.1606396445.1606396445.1; __utmz=253535702.1606396445.1.1.utmcsr=sh.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/; myfeet_tooltip=end; myLat=""; myLon=""; mcity=sh; spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT; f=n; commontopbar_new_city_info=2%7C%E4%B8%8A%E6%B5%B7%7Csh; commontopbar_ipcity=sh%7C%E4%B8%8A%E6%B5%B7%7C0; new_uv=2; utm_source=market; init_refer=https%253A%252F%252Fwww.baidu.com%252Fother.php%253Fsc.0f00000ZUeSZAyeHsgc69pxLD_quoJ_GKdnWkIa3SxGVfQ05sM6Bu9On4ri_VWa0gWkpM2-XoEGwIzPm0qfSgpWU3NEADXuKHRga8HhtGtiqUcbBzFCHV0BscDJ2x6_eYP0OVRfyYo9VXMjrHl-SdIQzCa2VMQlmD72LV3PHSd8dXUdx47PMPtvktelqNrz0k1Djx5-SmojtRlxk7WeoeNJFusPk.DY_NR2Ar5Od66z3PrrW6ButVvkDj3n-vHwYxw_vU85YIMAQV8qhORGyAp7WIu8L6.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqPHWPoQ5Z0ZN1ugFxIZ-suHYs0A7bgLw4TARqnsKLULFb5HR31pz1ksKzmLmqnfKdThkxpyfqnHRkrHDvrjRYPsKVINqGujYknWTknHbdP0KVgv-b5HDsPWTLPHbd0AdYTAkxpyfqnHDdn1f0TZuxpyfqn0KGuAnqHbG2RsKWThnqPH6vrHf%2526ck%253D6683.1.102.342.151.320.147.458%2526dt%253D16064378; wmda_session_id_11187958619315=1606437845774-c051ef42-6b02-6b6b; xxzl_cid=b4d63432bc2c4028b0b821140b9d515c; xzuid=13017688-3a96-40e0-b649-781581e5fc7e; new_session=0; wmda_session_id_1731916484865=1606437853667-3a5c6e36-6fd1-0246; sessionid=75f07cd0-2c83-406e-ac37-c28dfdbaaaee; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1606399987,1606400006,1606400240,1606437866; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B10104579731767; JSESSIONID=9CAF529F35AC49847AC95C0EB2C4C663; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1606439803",
    "referer": "https://sh.58.com/job.shtml?utm_source=market&spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT&PGTID=0d100000-0000-2de8-79cc-0ab220207b20&ClickID=2",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"

}

data = {
    "utm_source": "market",
    "spm": "u-2d2yxv86y3v43nkddh1.BDPCPZ_BT",
    "PGTID": "0d202408-0000-2aa1-20c2-500c20126847",
    "ClickID": "2"
}

time.sleep(5)
response = requests.get(url, headers=headers, data=data).text
print(response)
