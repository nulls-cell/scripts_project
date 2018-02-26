from random import randint


f = open("C:/Users/Administrator/Desktop/requirements.txt", 'w')
tem_str = 'abcde'
for i in range(5000):
    _count = randint(1, 3)
    write_str = ""
    for j in range(_count):
        num = randint(0, 4)
        write_str += tem_str[num]
    f.write(write_str+'\n')
f.close()
