import requests
import re
from bs4 import BeautifulSoup
import random
from datetime import timedelta, date
import datetime
import configparser
import matplotlib.pyplot as plt

# short https://www.notion.so/58951b5a29544562a93fd0c1f5d7112f?v=316bed45c314462c84dca09b30578cea&pvs=4
# query_id = "58951b5a29544562a93fd0c1f5d7112f"
# database_id = "316bed45c314462c84dca09b30578cea"
# https://www.notion.so/4d044f4888104a4c89fbe30487f0198f?v=49f70ebd825a4c85a2a13b9ea10180b8&pvs=4
config = configparser.ConfigParser()
config.read('../token.ini')
token = config.get('token', 'id')
database_id = config.get('database', 'short_database')  # 取database前边的
query_id = config.get('database', 'short_query')  # 取database前边的
headers = {
    "Authorization": "Bearer " + token,
    "accept": "application/json",
    "Notion-Version": "2022-06-28"  # Notion版本号
}
def DataBase_item_query(query_database_id):
    url_notion_block = 'https://api.notion.com/v1/databases/'+query_database_id+'/query'
    res_notion = requests.post(url_notion_block,headers=headers)
    S_0 = res_notion.json()
    res_travel = S_0['results']
    if_continue = len(res_travel)
    if if_continue>0:
        while if_continue%100 == 0:
            body = {
                'start_cursor' : res_travel[-1]['id']
            }
            res_notion_plus = requests.post(url_notion_block,headers=headers,json = body)
            S_0plus = res_notion_plus.json()
            res_travel_plus = S_0plus['results']
            for i in res_travel_plus:
                if i['id'] == res_travel[-1]['id']:
                    continue
                res_travel.append(i)
            if_continue = len(res_travel_plus)
    return res_travel
def get_page_information(page_id):
    url = 'https://api.notion.com/v1/pages/'+page_id
    notion_page = requests.get(url,headers=headers)
    result = notion_page.json()
    if notion_page.status_code == 200:
        print('页面属性获取成功')
    else:
        print('页面属性获取失败')

    return result
def relation_post(database_id):
    today_str = date.today().strftime('%Y-%m-%d')
    url = "https://api.notion.com/v1/pages"
    p = {"parent": {"database_id": database_id},
         "properties": {
             "Tags": {"select": {"name": "生词", "color": "yellow"}},
             "words": {"title": [{"type": "text", "text": {"content": "word_content"}}]},
             "passage": {"multi_select": [{"name": "001"}]},
             "phonetic symbol": {"rich_text": [{"type": "text", "text": {"content": "pronoun"}}]},
             "meaning": {
                 "rich_text": [{"type": "text", "text": {"content": "meaning"}}]},
             "Last": {"date": {"start": today_str}},
             "Next": {"date": {"start": today_str}},
             "voice": {"url": "voice_url"},
             "Level": {"select": {"name": "7", "color": "purple"}},
             "KnowAll": {"checkbox": False},
             "KnowSome": {"checkbox": False},
             "ForgetAll": {"checkbox": False},
#https://www.notion.so/291869fb8127414fbd5abb6fc1665dcc?v=19389f0bd13044ab9ad4df98f7ab99b8&pvs=4
#https://www.notion.so/001-230408-026-The-sonic-outernationalist-832eb1c98c1a4abda09e473d14ff7e70?pvs=4
#https://www.notion.so/064-8min-230729-Asia-Unsplendid-isolation-6c214fd7f70348728b21089c2318e243?pvs=4
# https://www.notion.so/002-0325-008-Leaders-How-the-EU-should-respond-to-American-subsidies-cfd93e8b93c44a73b08f474cb66e491e?pvs=4
             "relation": {
                 "relation":[

                     {
                         "id": "6c214fd7f70348728b21089c2318e243",

                     },
                     {
                         "id": "cfd93e8b93c44a73b08f474cb66e491e",

                     }
                 ]

                    # "synced_property_name": "064-8min-230729-Asia-Unsplendid isolation"
                  },
             # "Checkbox 1": {"checkbox": False},
             # "Checkbox 2": {"checkbox": False},
             # "Checkbox 3": {"checkbox": False},
             # "Checkbox 4": {"checkbox": False},
             # "Checkbox 5": {"checkbox": False},
             # "Checkbox 6": {"checkbox": False},
             # "Date Wrong": {"date": {"start": today}},
         },

         "children": [
             {
                 "type": "heading_3",
                 "heading_3": {
                     "rich_text": [{
                         "type": "text",
                         "text": {
                             "content": "sentence",
                         }
                     }],
                     "color": "default",
                     "is_toggleable": False,
                 }

             }
         ],
         }
    r = requests.post(url, json=p, headers=headers)
    print(r.text)

def relation_update():
    response = DataBase_item_query(query_id)
    all_page_id = []
    for dict in response:
        all_page_id.append(dict['id'])
# https://www.notion.so/word_content-cf64033553ac42b7b4e990ed91bfc3a0?pvs=4
#     res = get_page_information("cf64033553ac42b7b4e990ed91bfc3a0")

    relation_post(query_id)


if __name__ == "__main__":
    relation_update()