import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

def load_data(data_path):
    data = []
    with open(data_path, 'r') as fid:
        for line in fid:
            s = line.strip().split(' ')
            for l in s:
                ls = float(l)
                data.append(ls)
    return data

def save(segment, save_path, name):
    path = os.path.join(save_path, name)  # 分割后的存储路径
    if not os.path.exists(path):
        os.makedirs(path)
    index = len(segment)
    for i in range(index):
        sio.savemat(path+'/'+name+'_'+str(i+1)+'.mat', {'val': segment[i]})  # 存为mat格式

def heart_segment(data, segment_long, begin=0, end=None):
    '''
    :param data: 心电数据
    :param segment_long:分割采样点的个数
    :param begin: 分割数据的起点索引
    :param end: 分割数据的终点索引
    :return: 分割好的beat列表
    '''
    segment = []  # 二维数组，一行存储一条分割
    index_segment = []  # 记录分割点的索引
    if not end:
        end = len(data)
    while begin < end:
        index_segment.append(begin)
        begin = begin + segment_long
    # print('分割点的数量：', len(index_segment))

    for id in range(len(index_segment)):
        if id < len(index_segment)-1:
            seg = data[index_segment[id]:index_segment[id+1]]
            segment.append(seg)
    # print('数据分割后的形状')
    # print(np.shape(segment))
    return segment

# def plot_ecg(data, name, img_ecg):
#     x = range(len(data))
#     # plt.scatter(x, data, c='black', s=10)
#     # plt.axis('off')
#     plt.grid(True)  # 添加网格
#     plt.plot(data, c='r')
#     na =re.search("([a-z]+[\_][0-9]+[\_][0-9]+[\_][0-9]+[\_][0-9]+)",name).group()
#     # print(na)
#     path = os.path.join(img_ecg, na)  # 分割后的存储路径
#     if not os.path.exists(path):
#         os.makedirs(path)
#     # from io import BytesIO
#     # sio = BytesIO()
#     plt.savefig(path+'/'+name+'.png')
#     # plt.show()