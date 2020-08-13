from pprint import pprint
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
from datetime import datetime
import os
import csv


class Character(object):
    def __init__(self, character_id, name, introduction, wanteds, latest_wanted, published_dates, common_image_urls, whole_body_image_url='', avatar_image_url='', belonging='', skill1='', skill2='', skill3='', awakening=''):
        self.id = character_id
        self.name = name
        self.introduction = introduction
        self.wanteds = wanteds
        self.latest_wanted = latest_wanted
        self.published_dates = published_dates
        self.whole_body_image_url = whole_body_image_url
        self.avatar_image_url = avatar_image_url
        self.common_image_urls = common_image_urls
        self.belonging = belonging
        self.belonging_image_name = '%s_image_name' % belonging
        self.skill1 = skill1
        self.skill2 = skill2
        self.skill3 = skill3
        self.awakening = awakening
        self.whole_body_image_name = '%s_body_image_name' % character_id
        self.avatar_image_name = '%s_avatar_name' % character_id
        self.common_image_names = self.make_common_image_names(
            common_image_urls)

    def make_common_image_names(self, common_image_urls):
        names = []
        for index in range(len(common_image_urls)):
            name = 'common_image_name_%s' % str(index)
            names.append(name)
        return names

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'introduction': self.introduction,
            'belonging': self.belonging,
            'wanteds': self.wanteds,
            'latest_wanted': self.latest_wanted,
            'published_dates': self.published_dates,
            'belonging_image_name': self.belonging_image_name,
            'whole_body_image_url': self.whole_body_image_url,
            'whole_body_image_name': self.whole_body_image_name,
            'avatar_image_url': self.avatar_image_url,
            'avatar_image_name': self.avatar_image_name,
            'common_image_urls': self.common_image_urls,
            'common_image_names': self.common_image_names,
            'skill1': self.skill1,
            'skill2': self.skill2,
            'skill3': self.skill3,
            'awakening': self.awakening,
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

    base_url_path = 'https://onepiece.fandom.com/zh/wiki'
    english_name_xpath = '//div[@data-source="ename"]//div'
    whole_body_image_url_xpath = '//figure[@class="pi-item pi-image"]/a'
    description_xpath = '//meta[@name="description"]'
    belonging_xpath = '//div[@data-source="affiliation"]//a'

    characters = []
    failed_characters = []

    contents = load_json_file_to_dict_with_json_file_path(
        'one_piece_12:39:17/one_piece_wanted_ranking.json', 'characters')
    names = []
    hero_ids = []
    wanteds = []
    latest_wanteds = []
    published_dates = []
    for content_dict in contents:
        names.append(content_dict['name'])
        hero_ids.append(content_dict['hero_id'])
        wanteds.append(content_dict['wanteds'])
        latest_wanteds.append(content_dict['latest_wanted'])
        published_dates.append(content_dict['published_dates'])
    for (index, name) in enumerate(names):
        url_path = '%s/%s' % (base_url_path, name)
        pprint(url_path)
        if hero_ids[index] != '':
            driver.get(url_path)
            try:
                print("🤝start to get elements")
                english_name_elements = driver.find_elements_by_xpath(
                    english_name_xpath)
                description_elements = driver.find_elements_by_xpath(
                    description_xpath)
                whole_body_image_url_elements = driver.find_elements_by_xpath(
                    whole_body_image_url_xpath)
                belonging_elements = driver.find_elements_by_xpath(
                    belonging_xpath)
                if len(english_name_elements) > 0 and len(description_elements) > 0 and len(whole_body_image_url_elements) and len(belonging_elements) > 0:
                    english_name = driver.find_elements_by_xpath(
                        english_name_xpath)[0].text
                    description = driver.find_elements_by_xpath(description_xpath)[
                        0].get_attribute('content')
                    whole_body_image_url = driver.find_elements_by_xpath(whole_body_image_url_xpath)[
                        0].get_attribute('href')
                    belonging = driver.find_elements_by_xpath(belonging_xpath)[
                        0].get_attribute('title')
                    character = Character(
                        character_id=english_name,
                        name=name,
                        introduction=description,
                        wanteds=wanteds[index],
                        latest_wanted=latest_wanteds[index],
                        published_dates=published_dates[index],
                        whole_body_image_url=whole_body_image_url,
                        avatar_image_url=whole_body_image_url,
                        common_image_urls=[],
                        belonging=belonging
                    )
                    pprint('😎Successfully append %s in characters' % name)
                    characters.append(character)
                else:
                    failed_characters.append(name)
            except OSError:
                pprint('🚨 OS Error')
        else:
            failed_characters.append(name)
    dir_path = make_dir('one_piece_wanteds')
    json_file_name = 'one_piece_wanteds.json'
    to_encoded_json_with_object(
        'characters', characters, json_file_name, dir_path)
    pprint('🚀Successfully make one_piece_wanteds json file!')
    pprint('😱%s' % failed_characters)


get_character_introduction()
