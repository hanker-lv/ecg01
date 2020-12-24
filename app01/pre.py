import keras
import os
import re
import numpy as np
import scipy.io as sio
from app01 import data_pre

def predict(pre_path):
    #模型预测
    model_path = "./app01/saved/realtest/1602156286-947/0.330-0.837-020-0.275-0.864.hdf5"
    model = keras.models.load_model(model_path)
    # model.summary()

    # data = []
    ecg_out = []
    pre_mat = os.listdir(pre_path)
    for mat_file in pre_mat:
        f = os.path.join(pre_path, mat_file)
        if os.path.splitext(f)[1] == ".mat":
            ecg = sio.loadmat(f)['val'].squeeze()
            # data.append(ecg)
            ecg_ = ecg.reshape(1, -1, 1)
            # print(np.shape(ecg), type(ecg))
            predict = model.predict(ecg_)
            predict = np.argmax(predict, axis=2).squeeze()
            ecg_out.append(predict)
            # print(predict)
            # img_ecg = r'./data/ecg_img/'
            # data_pre.plot_ecg(ecg, mat_file[:-4], img_ecg)
    # print(len(data), type(data), data)
    # print(ecg_out)
    return ecg_out


def load_mat(name, index):
    data = []
    save_path = r'./data/seg/'
    mat_path = os.path.join(save_path, name)
    mat = os.listdir(mat_path)
    data_mat = mat[index]
    # print(data_mat)
    f = os.path.join(mat_path, data_mat)
    if os.path.splitext(f)[1] == ".mat":
        ecg = sio.loadmat(f)['val'].squeeze()
        data.append(ecg)
    return data


def handle_uploaded_file(f, path, time, name):
    """
    将浏览器上传的文件写入到path
    :param f: 上传的文件
    :param path: 写入文件的保存路径
    :param name: 文件的名称
    :return:
    """
    name_time = name + '_' + time
    file_path = os.path.join(path, name)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    #
    # dirs = os.listdir(file_path)
    with open(file_path+'/'+name_time + '.txt', 'wb') as f1:
        for i in f:
            f1.write(i)


def run_model(data_path, name, ecg_hz):
    save_path = r'./data/seg/'
    segment_time = 30  # 一个分割的时间长度（单位：秒）
    hz = int(ecg_hz)  # 采样频率
    segment_long = int(hz * segment_time)  # 一个分割采样点的个数
    # print(segment_long)
    # 读取原始数据
    data = data_pre.load_data(data_path)
    # print(len(data))
    # 分割原始数据
    seg = data_pre.heart_segment(data, segment_long)
    print(len(seg))
    data_pre.save(seg, save_path, name)
    # 模型预测
    pre_path = os.path.join(save_path, name)
    pres = predict(pre_path)
    # 将pres数组转换成列表
    pres_list = []
    for pre_i in pres:
        pre = list(pre_i)
        pres_list.append(pre)

    print(len(pres_list), pres_list)
    return pres_list


def make_classification(pres):
    classifications = []
    for pre in pres:
        #访问每个分割
        # print('pre1', pre)
        pre = list(set(pre))# 去重
        # print('pre2', pre)
        if len(pre) == 1: # 一个分割只有一个一个类别
            if pre[0] == 0:
                classification = 'AF'
            elif pre[0] == 1:
                classification = 'Normal'
            elif pre[0] == 2:
                classification = 'other'
            elif pre[0] == 3:
                classification = 'Noise'
            else:
                classification = 'error'
            classifications.append(classification)
        else:
            #  一个分割里的心拍 有多个类别的情况
            for pre_i in pre:
                if pre_i == 0:
                    classification = 'AF'
                elif pre_i == 1:
                    classification = 'Normal'
                elif pre_i == 2:
                    classification = 'other'
                elif pre_i == 3:
                    classification = 'Noise'
                else:
                    classification = 'error'
                classifications.append(classification)

    return classifications


def trans_num(strs):
    nums = []
    for str in strs:
        if str == 'AF':
            num = 0
        elif str == 'Normal':
            num = 1
        elif str == 'other':
            num = 2
        else:
            num = 3
        nums.append(num)
    # print(nums)
    return nums


def split_str(ecg_str):
    # 解析字符串
    ecg_str = ecg_str.replace("'", "")  # 把所有的’替换成空
    ecg_str = ecg_str.replace(" ", "")  # 把所有的空格替换成空
    # print(len(ecg_str), ecg_str)
    ecg_str = ecg_str[1:-1]  # 去掉最外层的‘[]'
    str = ecg_str.strip().split(',')
    # print(len(str), str)
    return str
