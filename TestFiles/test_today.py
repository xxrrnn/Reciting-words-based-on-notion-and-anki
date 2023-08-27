import requests
import re
from bs4 import BeautifulSoup
import random
from datetime import timedelta, date
import datetime
import configparser
import matplotlib.pyplot as plt
import os
from collections import OrderedDict
from datetime import datetime as dt

config = configparser.ConfigParser()
config.read('../token.ini')
token = config.get('token', 'id')
database_id = config.get('database', 'today_database')  # 取database前边的
query_id = config.get('database', 'today_query')  # 取database前边的
headers = {
"Authorization": "Bearer " + token,
"accept": "application/json",
"Notion-Version": "2022-06-28"  # Notion版本号
}

def delete_page(page_id):
    body = {
        'archived':True
    }
    url = 'https://api.notion.com/v1/pages/' + page_id
    notion = requests.patch(url, headers = headers, json = body)

    return 0
def DataBase_item_query(self):
    query_database_id = query_id
    url_notion_block = 'https://api.notion.com/v1/databases/' + query_database_id + '/query'
    res_notion = requests.post(url_notion_block, headers=headers)
    S_0 = res_notion.json()
    res_travel = S_0['results']
    if_continue = len(res_travel)
    print(len(res_travel))
    if if_continue > 0:
        while if_continue % 100 == 0:
            body = {
                'start_cursor': res_travel[-1]['id']
            }
            res_notion_plus = requests.post(url_notion_block, headers=headers, json=body)
            S_0plus = res_notion_plus.json()
            res_travel_plus = S_0plus['results']
            for i in res_travel_plus:
                if i['id'] == res_travel[-1]['id']:
                    continue
                res_travel.append(i)
            if_continue = len(res_travel_plus)
    return res_travel

def DataBase_item_delete(response):
    count = 0
    for dict in response:
        count += 1
        id = dict['id']
        print(count/ len(response), dict['properties']['words']['title'][0]['plain_text'])
        delete_page(id)




if __name__ == "__main__":
    response = DataBase_item_query(query_id)
    DataBase_item_delete(response)