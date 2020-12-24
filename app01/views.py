import os
import numpy as np
from django.shortcuts import render, redirect
from app01 import models, pre, data_pre
from login.views import login_required

# Create your views here.
@login_required
def index(request):
    """
    访问的主页
    :param request:
    :return:
    """
    all_person = models.Person.objects.all()
    # user_name = request.session.get('user_name')
    return render(request, 'index.html', locals())

@login_required
def person_index(request, person_id):
    person = models.Person.objects.get(pk=person_id)
    # print(person)
    request.session['person_id'] = person_id

    if person.sex == 'male':
        sex = '男'
    elif person.sex == 'female':
        sex = '女'
    # else:
    #     pass
    if models.EcgData.objects.filter(person_id=person_id):
        ecg = models.EcgData.objects.filter(person_id=person_id)
        return render(request, 'person_index.html', locals())
    else:
        error = '该用户暂时未查到ECG信息'
        return render(request, 'person_index.html', locals())

@login_required
def person_add(request):
    if request.method == 'GET':
        return render(request, 'person_add.html')
    else:
        # 新增用户
        person_name = request.POST.get('person_name')
        if not person_name:
            return render(request, 'person_add.html', {'error': '未输入用户'})
        if models.Person.objects.filter(name=person_name):
            return render(request, 'person_add.html', {'error': '用户已存在'})

        person_age = int(request.POST.get('person_age'))
        if not person_age:
            return render(request, 'person_add.html', {'error': '未输入年龄'})
        # print(person_name, person_age)
        person_sex = request.POST.get('sex')
        # 将数据新增到数据库中
        user_id = request.session['user_id']
        models.Person.objects.create(name=person_name, age=person_age, sex=person_sex, user_id=user_id)
        return redirect('/index/')

@login_required
def person_edit(request, person_id):
    # 修改用户数据
    person_obj = models.Person.objects.get(pk=person_id)

    if request.method == 'GET':
        return render(request, 'person_edit.html', locals())
    else:
        name = request.POST.get('person_name')
        age = request.POST.get('person_age')
        person_obj.name = name
        person_obj.age = age
        person_obj.save()
        return redirect('/person_index/{}'.format(request.session.get('person_id')))

@login_required
def upload(request, person_id):
    person = models.Person.objects.get(pk=person_id)
    if request.method == 'GET':
        return render(request, 'upload.html')
    else:
        # 获取用户提交的数据
        record_begin_time = request.POST.get('record_begin_time')
        ecg_time_hour = request.POST.get('ecg_time_hour')
        ecg_time_minute = request.POST.get('ecg_time_min')
        ecg_time_second = request.POST.get('ecg_time_second')
        ecg_time = ecg_time_hour + ':' + ecg_time_minute + ':' + ecg_time_second
        ecg_hz = request.POST.get('hz')
        file = request.FILES.get('file')
        # print(file)
        # 文件写入
        path = './data/upload_demo/'  # 上传文件保存的路径
        name = person.name
        import datetime
        now = datetime.datetime.now()
        time = now.strftime("%Y_%m_%d_%H%M%S")
        pre.handle_uploaded_file(file, path, time, name)
        # 将数据新增到数据库中
        models.EcgData.objects.create(record_begin_time=record_begin_time,
                                      ecg_time=ecg_time,
                                      person_id=person_id,
                                      ecg_path=(os.path.join(path, name) + '/' + name + '_' + time + '.txt'),
                                      ecg_hz=ecg_hz)
        # return HttpResponse('上传成功')
        return redirect('/person_index/{}'.format(request.session.get('person_id')))

@login_required
def ecg_model(request, person_id, ecg_id):
    ecg = models.EcgData.objects.get(pk=ecg_id, person_id=person_id)
    txt_path = ecg.ecg_path
    hz = ecg.ecg_hz
    data = []  # 按分割分的 所有分割的数据列表
    # # 获取原始所有心电数据
    # data = data_pre.load_data(txt_path)
    # 获取用户存储数据的文件名
    names = os.path.split(txt_path)[1]
    name = names[:-4]
    if ecg.ecg_result:
        # 判断是否已经预测过模型，如果已经运行过模型，则直接读取结果
        #解析字符串
        cls = pre.split_str(ecg.ecg_result)
        # print(np.shape(cls), cls)
        clss = list(set(cls))
        #  传递给前端的分类转化为数字的分类
        cls_num = pre.trans_num(cls)
        # 按分割获取每个分割的心电数据
        for i in range(len(cls)):
            data_i = pre.load_mat(name, i)
            data.append(data_i)
    else:
        message = '模型运行成功'
        # 预测指定的ECG
        predict = pre.run_model(txt_path, name, ecg.ecg_hz)
        # 获得预测的结果 cls为一个数组
        cls = pre.make_classification(predict)
        # print(np.shape(cls), cls)
        ecg.ecg_result = cls
        ecg.save()
        clss = list(set(cls))
        # print(predict)
        for i in range(len(cls)):
            data_i = pre.load_mat(name, i)
            data.append(data_i)

    return render(request, 'ecg_model.html', locals())

def annoation(request):
    return render(request, 'ann.html',locals())
