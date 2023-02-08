import requests


def gitlab_send_message(user, opt, branch, warehouse, id, message):
    """

    :param user:用户
    :param opt: git提交操作【push merge 等】
    :param branch: git 分支名称
    :param warehouse: git 仓库
    :param id: git id
    :param message: git commit 信息
    :return:
    """
    URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxx"
    HEADERS = {"Content-Type": "application/json"}
    Data = {
        "msgtype": "text",
        "text": {
            "content": f"{user} {opt} to branch {branch} at repository {warehouse} \n "
                       f"<font color=\"warning\">{id}</font>:<font color=\"comment\"> {message}</font>",
            "mentioned_list": [user],
        }
    }
    r = requests.post(url=URL, headers=HEADERS, json=Data, verify=False)
    print(r.json())


if __name__ == '__main__':
    # "https://github.com/YanHui-Yang/gitlab-robot"
    gitlab_send_message("peiqing.guo", "pushed", "develop", "Sudoku", "1f23cf45", "update:content of subtree 排序问题修复")
