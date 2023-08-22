import requests
# test_vocabularies
#https://www.notion.so/179911edeb864a8fa464fa1caf7ec3da?v=d7ca612cf0f641cca59a3d9b6d4e6284&pvs=4
# anki
#https://www.notion.so/4d044f4888104a4c89fbe30487f0198f?v=49f70ebd825a4c85a2a13b9ea10180b8&pvs=4
import configparser
config = configparser.ConfigParser()
config.read('token.ini')
token = config.get('token', 'id')


import requests

page_id = "4d044f4888104a4c89fbe30487f0198f"

url = "https://api.notion.com/v1/pages"

p = {"parent": {"database_id": page_id},
     "properties": {
         "Tags":{"select":{"name":"词组","color":"pink"}},
         "words": {"title": [{"type": "text", "text": {"content": "test_word"}}]},
         "meaning":{"rich_text": [{"type": "text", "text": {"content": "测试\n 单词 and english\n translation"}}]},
         "passage": {"multi_select": [{"name": "test"}]},
          "Checkbox 1": {"checkbox": False},
          "Checkbox 2": {"checkbox": False},
          "Checkbox 3": {"checkbox": False},
          "Checkbox 4": {"checkbox": False},
          "Checkbox 5": {"checkbox": False},
          "Checkbox 6": {"checkbox": False},
         "Date Wrong": {"date": {"start": "2023-08-15"}},
         # "Date Wrong": {"date": {"start": "2021-05-11T11:00:00.000-04:00", "end": "2021-05-12T11:00:00.000-04:00"}},
         "phonetic symbol": {"rich_text": [{"type": "text", "text": {"content": "/音标我不会打/"}}]},
         "voice": {"url": "https://notion.so/notiondevs"},

     },

     "children": [

         {
             "type": "heading_3",
             "heading_3": {
                 "rich_text": [{
                     "type": "text",
                     "text": {
                         "content": "这里是",
                     }
                 }],
                 "color": "default",
                 "is_toggleable": False,
             }

         }

     ],

     }

headers = {

    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
}

r = requests.post(url, json=p, headers=headers)
print(r.text)
if r.status_code == 200:
    print("导入Notion成功！")
else:
    print("导入Notion失败！")