from pprint import pprint
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
from datetime import datetime
import shutil
import os
from os import listdir
from os.path import isfile, isdir, join
import csv
from distutils.dir_util import copy_tree


# os 相關操作
def make_dir_with_time_stamp(dir_name):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H:%M")
    # .split(' ')[1]
    dir_path = './%s_%s' % (dir_name, dt_string)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def make_dir(dir_name):
    dir_path = './%s' % (dir_name)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def make_dir_under_dir_path(dir_path, detail):
    youtuber_dir_path = '%s/%s' % (
        dir_path, detail)
    os.makedirs(youtuber_dir_path, exist_ok=True)
    return youtuber_dir_path


def get_all_folders(dir_path):
    all_dir_paths = []
    files = listdir(dir_path)
    for f in files:
        fullpath = join(dir_path, f)
        if isdir(fullpath):
            all_dir_paths.append(fullpath)
    return all_dir_paths


def get_all_files(dir_path):
    all_file_paths = []
    files = listdir(dir_path)
    for f in files:
        fullpath = join(dir_path, f)
        if isfile(fullpath):
            all_file_paths.append(fullpath)
    return all_file_paths


def copy_dir_to_dir(original_path, target_path):
    copy_tree(original_path, target_path)


def copy_file_to_dir(original_file_path, target_dir_path):
    shutil.copy(original_file_path, target_dir_path)


def move_to(original_path, target_path):
    shutil.move(original_path, target_path)


# photo parser
def get_photo(url, file_saved_dir_path, file_name):
    header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'
    file_name = '%s.jpg' % file_name
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', header)]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(
        url, '%s/%s' % (file_saved_dir_path, file_name))


# text formatted
def formatted_number(number):
    number_str = ''
    if int(number / 100000000) > 0:
        if str(int(number / 10000000))[-1] == '0':
            number_str = '%s億' % (int(number / 100000000))
        else:
            number_str = '%s億%s千萬' % (int(number / 100000000),
                                      str(int(number / 10000000))[-1])

    elif int(number / 10000) > 0:
        number_str = '%s萬' % int(number / 10000)
    else:
        number_str = str(number)
    return number_str

# 取小數點後幾位


def get_two_float(self, f_str, n=2):
    f_str = str(f_str)
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]
    return float(".".join([a, c]))

# json encode and decode


def load_json_file_to_dict_with_json_file_path(json_file_path, object_key):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        output = json.load(f)['results'][0][object_key]
        return output


def to_encod_json_with_dict(obj_key, obj_dict, json_file_name, json_file_folder_path):
    overall_dic = dict()
    overall_dic[obj_key] = obj_dict
    jsonStr = json.dumps({"results": [overall_dic]},
                         ensure_ascii=False, separators=(',\n', ': '))
    json_path = '%s/%s' % (json_file_folder_path, json_file_name)
    file = open(json_path, 'w', encoding='UTF-8')
    file.write(jsonStr)
    file.close()
    return json_path


def to_encoded_json_with_objects(obj_key, objects, json_file_name, json_file_folder_path):
    overall_dic = dict()
    results = [obj.to_dict()
               for obj in objects]
    overall_dic[obj_key] = results
    jsonStr = json.dumps({"results": [overall_dic]},
                         ensure_ascii=False, separators=(',\n', ': '))
    json_path = '%s/%s' % (json_file_folder_path, json_file_name)
    file = open(json_path, 'w', encoding='UTF-8')
    file.write(jsonStr)
    file.close()
    return json_path


def load_json_file_to_dict(json_path, obj_key):
    # json_path = './%s/%s' % (json_file_folder_path, json_file_name)
    with open(json_path, 'r', encoding='utf-8') as f:
        output = json.load(f)['results'][0][obj_key]
        return output


def read_csv_content(csv_file_path, fieldnames):
    csv_file = open(csv_file_path, 'r', encoding='utf-8')
    # fieldnames = ("mandarin_name", "character_image", "introduction", "skill1",
    #               "skill2", "skill3", "awakening", "health", "mojo", "resistant", "comic_name", "tier")
    row_dicts = csv.DictReader(csv_file, fieldnames)
    return row_dicts


def sorted_file_with_key(json_file_path, obj_key, sorted_key, reverse=False):
    dicts = load_json_file_to_dict(json_file_path, obj_key)
    dicts.sort(
        key=lambda x: x[sorted_key], reverse=reverse)
    dir_name = '%s_sorted_by_%s' % (
        json_file_path.split('/')[-1].split('.')[0], sorted_key)
    dir_path = make_dir(dir_name)
    to_encod_json_with_dict(
        obj_key=obj_key,
        obj_dict=dicts,
        json_file_name='%s.json' % dir_name,
        json_file_folder_path=dir_path)
    return dicts


def reverse_file(file_path, object_key):
    file_name = '%s_reversed.json' % file_path.split(
        '/')[-1].replace('.json', '')
    removed_str = file_path.split('/')[-1]
    dir_path = file_path.replace(removed_str, '')
    content_dicts = load_json_file_to_dict_with_json_file_path(
        file_path, object_key)
    content_dicts.reverse()
    to_encod_json_with_dict(
        object_key, content_dicts, file_name, dir_path)


def make_txt(json_file_path, text, obj_key):
    file_name = '%s_text' % json_file_path.split('/')[-1].split('.')[-2]
    removed_str = json_file_path.split('/')[-1]
    dir_path = json_file_path.replace(removed_str, '')
    file_path = "%s/%s.txt" % (dir_path, file_name)
    text_file = open(file_path, "w")
    n = text_file.write(text)
    text_file.close()
    return file_path


# 產生 July, 2020 格式的日期
def formate_date(date_str):
    published_date_time = datetime.strptime(
        date_str, "%m, %Y")
    return published_date_time.strftime("%B, %Y")
