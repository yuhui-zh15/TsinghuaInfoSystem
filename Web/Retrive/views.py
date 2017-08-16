#coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render
import gl
import re
import chardet
import jieba
import datetime

cur_page = 0

def get_content(keylist, file):
    #注意文件路径
    fileopen = open('./list/' + file)
    content = fileopen.read()
    content = content.decode('utf-8')
    fileopen.close()
    dr = re.compile(r"<p.*?</p>", re.I|re.S|re.M)
    items = re.findall(dr, content)
    content = ""
    for item in items:
        content = content + item
    dr = re.compile(r'<[^>]+>')
    content = dr.sub('',content)
    if len(content) > 200:
        content = content[0: 200] + '...'
    for key in keylist:
        content = content.replace(key, u'<font color="orange">' + key + u'</font>')
    return content

def get_items(keylist, files):
    items = []
    if (len(files) != 0):
        for i in range(cur_page * 12, min((cur_page + 1) * 12, len(files))):
            dict_ = dict()
            dict_['title'] = gl.m_file2title.get(files[i][0])[7: -8]
            dict_['time'] = gl.m_file2time.get(files[i][0])       
            dict_['text'] = get_content(keylist, files[i][0])
            dict_['url'] = gl.m_file2url.get(files[i][0])
            items.append(dict_)
    else:
        dict_ = dict()
        dict_['title'] = 'None'
        dict_['time'] = 'None'         
        dict_['text'] = 'No result!'
        dict_['url'] = ''
        items.append(dict_)
    return items

def filters(files, arg):
    retfiles = []
    for file in files:
        if (len(file[0]) < 20): continue
        filedate = datetime.date(int(file[0][0:4]), int(file[0][4:6]), int(file[0][6:8]))
        datedelte = datetime.date.today() - filedate
        if (arg == 'year' and datedelte < datetime.timedelta(365)): retfiles.append(file)
        elif (arg == 'month' and datedelte < datetime.timedelta(30)): retfiles.append(file)
        elif (arg == 'week' and datedelte < datetime.timedelta(7)): retfiles.append(file)
        elif (arg == 'day' and datedelte < datetime.timedelta(1)): retfiles.append(file)
        elif (arg ==''): retfiles.append(file)
    return retfiles

def retrive(request):
    global cur_page
    if request.GET.has_key('key'):
        print 'start'
        key = request.GET['key']
        key = key.replace(' ', '')
        keylist_ = jieba.cut(key)
        keylist = []
        for item in keylist_:
            keylist.append(item)
        print 'make dict'
        file2num = dict()
        for item in keylist:
            keyfile = gl.m_dict.get(item)
            if (keyfile == None): continue
            cnt = 0
            for file in keyfile:
                if (file in file2num.keys()):
                    file2num[file] = file2num[file] + 1
                else:
                    file2num[file] = 1
                cnt = cnt + 1
                if (cnt > 5000): break
        file2num = file2num.items()
        print 'filter'
        if request.GET.has_key('filter'):
            arg = request.GET['filter']
        else:
            arg = ''
        file2num = filters(file2num, arg)
        file2num = sorted(file2num, key = lambda x: x[0], reverse=True)
        file2num = sorted(file2num, key = lambda x: x[1], reverse=True)
        print 'change page'
        if request.GET.has_key('prev'):
            if (cur_page > 0): cur_page -= 1
        elif request.GET.has_key('next'):
            if ((cur_page + 1) * 12 < len(file2num)): cur_page += 1
        else:
            cur_page = 0
        print 'get items'
        items = get_items(keylist, file2num)
        print 'return'
        return render(request, 'result.html', {'key':key, 'items':items,})
    else:
        key = ""
        return render(request, 'retrive.html')

