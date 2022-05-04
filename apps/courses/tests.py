from django.test import TestCase

# Create your tests here.
from ExaminationManage.settings import UPLOAD_PATH

if __name__ == '__main__':
    with open('../../{}/{}'.format(UPLOAD_PATH, 'subject_.16516487178541042.csv'), "r", encoding='UTF-8') as fsr:
        # 去掉首行
        fsr.readline()
        line = fsr.readline()
        while line:
            print(line)
            line = fsr.readline()
