from pprint import pprint
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
from datetime import datetime
import os
import csv
import Utilities

class Onepiece_content(object):
    def __init__(self, description, image_url):
        self.description = description
        self.image_url = image_url
        
    def to_dict(self):
        return {
            'description': self.description,
            'image_url': self.image_url
        }

def make_dir(dir_name):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").split(' ')[1]
    youtuber_dir_path = './%s_%s' % (dir_name, dt_string)
    os.makedirs(youtuber_dir_path, exist_ok=True)
    return youtuber_dir_path


def make_dir_under_dir_path(dir_path, detail):
    youtuber_dir_path = '%s/%s' % (
        dir_path, detail)
    os.makedirs(youtuber_dir_path, exist_ok=True)
    return youtuber_dir_path


def to_encoded_json_with_object(obj_key, objects, json_file_name, json_file_folder_path):
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


def load_json_file_to_dict_with_json_file_path(json_file_path, object_key):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        output = json.load(f)['results'][0][object_key]
        return output

def get_movie_info(language='TW'):
    chrome_options = Options()  # 啟動無頭模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)

    all_info = load_json_file_to_dict_with_json_file_path('one_piece_movies_01:10:37/one_piece_movies.json', 'movies')
    all_urls = all_info[0]['movie_url']


    description=[]
    image_url=[]

    try:

        for each_url in all_urls:
            driver.get(each_url)
            print('🎁 now getting %s info' % each_url)
            elements_description = driver.find_elements_by_css_selector('p+ p , h2+ p , .pi-layout-default+ p')
            elements_image_url = driver.find_elements_by_css_selector('.pi-image-thumbnail')

            description.append([ele.text for ele in elements_description])
            image_url.append([ele.get_attribute('src') for ele in elements_image_url])

        joined_description=[]

        for record in description:
            joined_record = ''.join(record)
            joined_description.append(joined_record)
        


        

        onepiece_content = Onepiece_content(
            description = joined_description,
            image_url = image_url,
        )
        onepieces_content =[]
        onepieces_content.append(onepiece_content)

    except OSError:
        print('😍 OSError')

    dir_path = make_dir('one_piece_contents')
    json_file_name = 'one_piece_contents.json'
    to_encoded_json_with_object(
        'movie_info', onepieces_content, json_file_name, dir_path)

get_movie_info()
