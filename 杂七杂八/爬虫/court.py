import requests
import json
import time
import random
import threading
import queue

headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'referer': 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo'}
url = "https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1"

from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append(["公告人", "当事人", "公告类型", "发布时间", "正文"])


def spider(num):
    for i in range(num):
        l = '[{"name":"sEcho","value":0},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":'
        r = '},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]'
        temp = l + str(i * 15) + r
        formdata = {
            "_noticelist_WAR_rmfynoticeListportlet_content": "",
            "_noticelist_WAR_rmfynoticeListportlet_searchContent": "",
            "_noticelist_WAR_rmfynoticeListportlet_courtParam": "",
            "_noticelist_WAR_rmfynoticeListportlet_IEVersion": "ie",
            "_noticelist_WAR_rmfynoticeListportlet_flag": "init",
            "_noticelist_WAR_rmfynoticeListportlet_noticeType": "",
            "_noticelist_WAR_rmfynoticeListportlet_noticeTypeVal": "全部",
            "_noticelist_WAR_rmfynoticeListportlet_aoData": temp,
        }

        res = requests.post(url, data=formdata).text
        res = json.loads(res)
        time.sleep(random.random())

        for item in res["data"]:
            uuid = item["uuid"]
            formdata1 = {
                "_noticedetail_WAR_rmfynoticeDetailportlet_uuid": uuid
            }
            new_url = "https://rmfygg.court.gov.cn/web/rmfyportal/noticedetail?p_p_id=noticedetail_WAR_rmfynoticeDetailportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=noticeDetail&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1"
            response = requests.post(new_url, data=formdata1,
                                     headers={'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}).text
            response = json.loads(response)
            # 公告人
            notice_people = response["court"]
            # 当事人
            parties_concerned = response["tosendPeople"]
            # 公告类型
            notice_type = response["noticeType"]
            # 发布时间
            release_time = response["publishDate"]
            # 正文
            content = response["noticeContent"]
            print("公告人", notice_people)
            print("当事人", parties_concerned)
            print("公告类型", notice_type)
            print("发布时间", release_time)
            print("正文", content)
            print("-" * 120)

            line = [notice_people, parties_concerned, notice_type, release_time, content]
            ws.append(line)
            wb.save("court.xlsx")


if __name__ == '__main__':
    num = 10

    for i in range(10):
        t = threading.Thread(target=spider(num))
        t.start()
    t.join()
