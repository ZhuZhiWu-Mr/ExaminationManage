from django.test import TestCase

# Create your tests here.
#
def handle_single_choice():
    """
    处理单选题
    ['<p>发的课件撒结果大家法律的凯撒奖霏霏械</p><p>A.123</p><p>B.rekwjqkl</p><p>C.fdjsagklj</p>']
    """
    test_data = '<p>发的课件撒结果大家法律的凯撒奖霏霏械</p><p>A.123</p><p>B.rekwjqkl</p><p>C.fdjsagklj</p>'.replace('<p>', '')
    print(test_data)
    test = test_data.split('</p>')[0:-1]
    print(test)

if __name__ == '__main__':
    list_t = ['2', '3', '2']
    tes, *b = list_t
    print(b)
    # print(list_t)
    # print(str(list_t))
    # print(list(str(list_t)))
    # # handle_single_choice()