
# coding: utf-8
import md_search_image
import numpy as np
import os
import sys

def download_md_image(path=None):
    file_list,dir_list = md_search_image.dir_list(path)
    file_path_list = np.array(file_list[:,0])
    file_name_list = np.array(file_list[:,1])
    list_search_index = np.core.defchararray.find(file_path_list,'.md')    #numpy字串搜尋，無找到為-1，返回索引
    list_search_index = np.flatnonzero(list_search_index>0)      #轉成bool傳回非0索引
    md_file_path = file_path_list[list_search_index]
    md_file = file_name_list[list_search_index]
    for file_num in range(len(md_file)):
        file_name = md_file[file_num]
        file_path = os.path.join(path,file_name)
        save_dir_path = md_search_image.create_dir(path,file_name[:-3])
        file = open(file_path,'r',encoding='utf-8')
        file.seek(0)
        md_data = file.read()
        start_list = md_search_image.search_data(md_data,"\!\[")
        file_exist_flag = 1
        if len(start_list) == 0:
            print('image does not exist in the file:',str(file_name))
            file_exist_flag = 0
        if file_exist_flag == 1:
            data = md_search_image.search_content0(md_data,start_list)
            new_start_list = np.array(data[1])[:,1]
            data2 = md_search_image.search_content1(md_data,new_start_list)
            image_html_list = data2[0]
            print(file_name,'\n',np.array(image_html_list))
            for num in range(len(image_html_list)):
                save_name = save_dir_path+'\\'+ file_name+str(num)+'.png'
                md_search_image.request_download(image_html_list[num][1:-1],save_name)

if __name__ == "__main__":
    if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]) == True:
        path = sys.argv[1]
        download_md_image(path)
    else:
        print("Usage: python3 "+ 'file_name ' + 'dir_path')
