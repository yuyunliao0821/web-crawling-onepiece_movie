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

class Onepiece_movie(object):
    def __init__(self, movie_url, mandarin_title, published_date, runtime, revenue):
        self.movie_url = movie_url
        self.mandarin_title = mandarin_title
        self. published_date = published_date
        self.runtime = runtime
        self.revenue = revenue
        
    def to_dict(self):
        return {
            'movie_url': self.movie_url,
            'mandarin_title': self.mandarin_title,
            'published_date': self.published_date,
            'runtime': self.runtime,
            'revenue': self.revenue,
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

def get_character_introduction(language='TW'):
    chrome_options = Options()  # 啟動無頭模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)

    url_path = 'https://onepiece.fandom.com/zh/wiki/%E5%8A%87%E5%A0%B4%E7%89%88'
    driver.get(url_path)
    print('🎁 get url path')


    try:
        pprint('🎁 start to find element')
        elements_url=[]
        elements_title=[]
        elements_published_date=[]
        elements_runtime=[]
        elements_revenue=[]

        for i in range(2,16):
            elements_url += driver.find_elements_by_xpath('//*[@id="mw-content-text"]/table[1]/tbody/tr[%s]/td[2]/p/a'% i)
            elements_title += driver.find_elements_by_xpath('//*[@id="mw-content-text"]/table[1]/tbody/tr[%s]/td[2]'% i)
            elements_published_date += driver.find_elements_by_xpath('//*[@id="mw-content-text"]/table[1]/tbody/tr[%s]/td[3]'% i)
            elements_runtime += driver.find_elements_by_xpath('//*[@id="mw-content-text"]/table[1]/tbody/tr[%s]/td[4]'% i)
            elements_revenue += driver.find_elements_by_xpath('//*[@id="mw-content-text"]/table[1]/tbody/tr[%s]/td[5]'% i)

        movie_urls =[ele.get_attribute('href') for ele in elements_url]
        titles =[ele.text for ele in elements_title]
        published_date =[ele.text for ele in elements_published_date]
        runtime =[ele.text for ele in elements_runtime]
        revenue =[ele.text for ele in elements_revenue]

        onepiece = Onepiece_movie(
            movie_url = movie_urls,
            mandarin_title = titles,
            published_date = published_date,
            runtime = runtime,
            revenue = revenue
        )
        onepieces =[]
        onepieces.append(onepiece)

    except OSError:
        pprint('😍 OSError')

    dir_path = make_dir('one_piece_movies')
    json_file_name = 'one_piece_movies.json'
    to_encoded_json_with_object(
        'movies', onepieces, json_file_name, dir_path)

get_character_introduction()
