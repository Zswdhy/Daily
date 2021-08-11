import subprocess
import os


def word_to_pdf():
    # 需要将github下载的docx2pdf文件放到当前目录下
    subprocess.run(f'docx2pdf {path2}')
    os.remove(path2)


if __name__ == "__main__":
    path2 = 'medical_details.docx'
    word_to_pdf()