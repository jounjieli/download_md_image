# coding: utf-8
from os import listdir
from os.path import isfile, isdir, join
import numpy as np
import re
import requests
import numpy as np
import os
import sys
import pathlib
from urllib.parse import urlparse

def Get_dir_list(path):
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
            file_list = np.append(file_list,[[mypath+'\\'+f,f]],axis=0)
        elif isdir(fullpath):
            dir_list = np.append(dir_list,[[mypath+'\\'+f,f]],axis=0)
    file_list = file_list[1:]
    dir_list = dir_list[1:]
    return [file_list,dir_list]


def request_download(IMAGE_URL,save_name):
    """save_name = path + file name"""
    headers = {'User-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"}
    r = requests.get(IMAGE_URL,headers=headers)
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

def download_md_image(root_path=None):
    file_list,dir_list = Get_dir_list(root_path)
    file_path_list = np.array(file_list[:,0])
    file_name_list = np.array(file_list[:,1])
    list_search_index = np.core.defchararray.find(file_path_list,'.md')    #numpy字串搜尋，無找到為-1，返回索引
    list_search_index = np.flatnonzero(list_search_index>0)      #轉成bool傳回非0索引
    md_file_path = file_path_list[list_search_index]
    md_file = file_name_list[list_search_index]
    for file_num in range(len(md_file)):        
        file_full_name = md_file[file_num]
        file_name = os.path.splitext(file_full_name)[0] 
        file_ext = os.path.splitext(file_full_name)[1] 
        file_path = os.path.join(root_path, file_full_name)
        new_md_path = os.path.join(root_path, file_name, "NewLocalMarkdown_" + file_full_name)
        file = open(file_path,'r',encoding='utf-8')
        file.seek(0)
        md_data = file.read()
        new_md_data = md_data
        start_list = search_data(md_data,"\!\[")
        file_exist_flag = 1
        if len(start_list) == 0:
            print('image does not exist in the file:',str(file_name))
            file_exist_flag = 0
        if file_exist_flag == 1:
            data = search_content0(md_data,start_list)
            new_start_list = np.array(data[1])[:,1]
            data2 = search_content1(md_data,new_start_list)
            image_html_list = data2[0]
            print(file_name,'\n', np.array(image_html_list))
            for num in range(len(image_html_list)):
                image_url = image_html_list[num][1:-1]
                image_full_name = urlparse(image_url).path.split('/')[-1]
                image_name = os.path.splitext(image_full_name)[0]
                image_ext = os.path.splitext(image_full_name)[1]
                os.makedirs(os.path.join(root_path, file_name, "image"), exist_ok=True)
                image_path = os.path.join(root_path, file_name, "image", image_full_name)                
                request_download(image_url, image_path)                
                # search
                relative_image_path = str(pathlib.Path(image_path).relative_to(os.path.join(root_path, file_name)))              
                new_md_data = new_md_data.replace(image_html_list[num], r"({0})".format(relative_image_path))
        with open(new_md_path, "w", encoding="utf8") as f:
            f.write(new_md_data)
