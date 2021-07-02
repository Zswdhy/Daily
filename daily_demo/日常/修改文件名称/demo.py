import os
import re


def rename_func(path):
    for file in os.listdir(path):
        print('判断', os.path.isfile(path + '/' + file), type(os.path.isfile(path + '/' + file)))
        #  判断当前路径是否是文件
        if not os.path.isfile(path + '/' + file):
            rename_func(path + '/' + file)
        else:
            if '：' in file:
                new_name = re.sub(r'.*：', '', file)
                os.rename(path + '/' + file, path + '/' + new_name)
            elif '新课标高中数学人教A版必修五全册课件' in file:
                new_name = file.replace('新课标高中数学人教A版必修五全册课件', '')
                os.rename(path + '/' + file, path + '/' + new_name)
            elif '高中数学人教A版必修5' in file:
                new_name = file.replace('高中数学人教A版必修5', '')
                os.rename(path + '/' + file, path + '/' + new_name)


if __name__ == '__main__':
    path = '文件'
    rename_func(path)
