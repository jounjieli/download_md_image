
# coding: utf-8

from os import listdir
from os.path import isfile, isdir, join
import numpy as np
import re
import requests
import os

def dir_list(path):
    """
    path:指定要列出所有檔案的目錄
    return: list
     list[0] = file_list
     list[1] = dir_list
    """
    mypath = path
    files = listdir(mypath)
    file_list = np.zeros([1,2])
    dir_list = np.zeros([1,2])
    for f in files:
        fullpath = join(mypath, f)
        if isfile(fullpath):
            file_list = np.append(file_list,[[join(mypath,f),f]],axis=0)
        elif isdir(fullpath):
            dir_list = np.append(dir_list,[[join(mypath,f),f]],axis=0)
    file_list = file_list[1:]
    dir_list = dir_list[1:]
    return file_list,dir_list

def create_dir(path,dir_name):
    """
    創資料夾
    """
#     path = os.path.join(str(path),str(dir_name))
    path = str(path) + '\\' + str(dir_name)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path

def request_download(image_url,save_name):
    """save_name = path + file name"""
    headers = {'User-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"}
    r = requests.get(image_url,headers=headers)
    with open(save_name, 'wb') as f:
        f.write(r.content)

def search_content0(data,statr_list):
    """[]"""
    content = []
    offset = []
    for num in range(len(statr_list)):
        index_val = statr_list[num]
        search_range = data[index_val:]
        index_val_1 = re.search('\]',search_range).span()[1]
        search_num = len(re.findall('\[',search_range[:index_val_1]))
        search_str = ''
        for __ in range(search_num):
            search_str = search_str + '[^\]]*\]'
        index_val_2 = re.search(search_str,search_range).span()[1]
        content.append(data[index_val:index_val+index_val_2])
        offset.append((index_val,index_val+index_val_2))
    return [content,offset]

def search_content1(data,statr_list):
    """()"""
    content = []
    offset = []
    for num in range(len(statr_list)):
        index_val = statr_list[num]
        search_range = data[index_val:]
        index_val_1 = re.search('\)',search_range).span()[1]
        search_num = len(re.findall('\(',search_range[:index_val_1]))
        search_str = ''
        for __ in range(search_num):
            search_str = search_str + '[^\)]*\)'
        index_val_2 = re.search(search_str,search_range).span()[1]
        content.append(data[index_val:index_val+index_val_2])
        offset.append((index_val,index_val+index_val_2))
    return [content,offset]

def search_data(data,pattern):
    iter_object = re.finditer(pattern,data)
    start_offset_list = []
    for _ in iter_object:
        start = _.span()[0]
        start_offset_list.append(start)
    return start_offset_list
