# -*- coding: utf-8 -*-
import os
import sys
import xlrd
import xlsxwriter
from tqdm import tqdm


def find_miss_post(filepath):
    filename_list = []
    for file in os.listdir(filepath):
        if file.endswith('xlsx'):
            filename_list.append(int(file.split('.')[0]))
    filename_list.sort()
    max_post = filename_list[-1]
    for ele in range(0, max_post):
        if (ele+1) not in filename_list:
            print(str(ele)+' is not exist')


# 获取目录下的所有文件名
def get_filename(tar_path):
    filename_list = []
    for file in os.listdir(tar_path):
        if file.endswith('xlsx'):
            filename_list.append(int(file.split('.')[0]))
    filename_list.sort()
    filename = []
    for file in filename_list:
        filename.append(tar_path+'/'+str(file)+'.xlsx')
    return filename


def concat_and_insert(f_dir):
    records = []
    print('read xlsx')
    for ai in tqdm(f_dir):
        # 读文件
        data = xlrd.open_workbook(ai)
        # 第一个sheet页的名称
        first_sheet = data.sheet_by_index(0).name
        # print(ai, '>'*10, first_sheet)
        # 获取sheet页的名称
        sheet = data.sheet_by_name(first_sheet)
        # 获取表的行数
        n_rows = sheet.nrows
        if n_rows == 0:
            print(ai+' is empty')
        for i in range(n_rows):
            records.append(sheet.row_values(i))
    return records


def write_file(alist, tar_name):
    tarfile = tar_name + '.xlsx'
    print('write '+tarfile)
    w_new = xlsxwriter.Workbook(tarfile)
    w_add = w_new.add_worksheet(tar_name)
    for row_num, row_data in enumerate(alist):
        w_add.write_row(row_num, 0, row_data)
    w_new.close()


if __name__ == '__main__':
    file_path = sys.argv[1]

    find_miss_post(file_path)

    file_name = get_filename(file_path)

    records_all = concat_and_insert(file_name)

    tarname = file_path
    write_file(records_all, tarname)
