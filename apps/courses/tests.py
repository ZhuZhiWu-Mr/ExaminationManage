import random

from django.test import TestCase

# Create your tests here.
from ExaminationManage.settings import UPLOAD_PATH

if __name__ == '__main__':
    a = random.sample([1,2,3,4], 7)
    print(a)
