import matplotlib as mlt
mlt.use('Agg')
import matplotlib.pyplot as plt
import numpy as np




# 折线图
def make_line(x_data_list, y_data_lists, labels, save_path=None):
    assert(len(x_data_list) == len(y_data_lists[0]) and len(x_data_list) == len(labels))
    for i in range(len(y_data_lists)):
        assert(isinstance(y_data_lists[i], list))
        plt.plot(x_data_list, y_data_lists[i], label=labels[i])
    #plt.





x = np.linspace(0, 5, 10)
y = np.array([a for a in x])
x2 = np.linspace(0, 5, 10)
y2 = np.array([a*2 for a in x2])
plt.plot(x, y, label='first')
plt.plot(x2, y2, label='second')
# x轴标签
plt.xlabel('Plot Number')
# y轴标签
plt.ylabel('Important var')
# 主标题
plt.title('Interesting Graph\nCheck it out')
# 生成默认图例，在plt.plot()中设置了label属性后才会生效
plt.legend()
plt.show()
plt.savefig('aaaaa.jpg',r'C:\Users\Administrator\Desktop')

