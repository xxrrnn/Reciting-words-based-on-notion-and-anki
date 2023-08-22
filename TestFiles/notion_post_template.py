import requests

# https://www.notion.so/0ed7e11a059b4787a8b0b5521688021d?v=4388b0a1b8404392b19a941f812c9617&pvs=4
# https://www.notion.so/69c5864cb490478cb3357abe8bb18998?v=b6573b4ba4a24fbfa946247ffcdd604a&pvs=4
# https://www.notion.so/000c9e8a7b6f4662acd45726e3e7ae57?pvs=4


import requests

page_id = "69c5864cb490478cb3357abe8bb18998"

url = "https://api.notion.com/v1/pages"

p = {"parent": {"database_id": page_id},

     "properties": {
         "标题": {"title": [{"type": "text", "text": {"content": "BA"}}]},
         "数字": {"number": 88},
         "单选": {"select": {"name": "中国", "color": "blue"}},
         "多选": {"multi_select": [{"name": "选项1"}, {"name": "选项2"}]},
         "文本": {"rich_text": [{"type": "text", "text": {"content": "这是一段文字"}}]},
         "清单": {"checkbox": True},
         "状态": {"status": {"name": "In progress"}},
         "日期": {"date": {"start": "2021-05-11T11:00:00.000-04:00", "end": "2021-05-12T11:00:00.000-04:00"}},
         "附件": {"files": [{"type": "external", "name": "资料包",
                             "external": {"url": "https://website.domain/images/space.png"}}]
                  },
         "网址": {"url": "https://notion.so/notiondevs"},
         "邮箱": {"email": "hello@test.com"},
         "电话": {"phone_number": "415-000-1111"}

     },

     "children": [
         {
             "type": "image",
             "image": {
                 "type": "external",
                 "external": {
                     "url": "https://www.biografiacortade.com/wp-content/uploads/2019/04/karl1-258x300.jpg"
                 }
             }
         },

         {
             "type": "paragraph",
             "paragraph": {
                 "rich_text": [{
                     "type": "text",
                     "text": {
                         "content": "这是一段正文",

                     }
                 }],
                 "color": "default",

             }
         },

         {
             "type": "heading_1",
             "heading_1": {
                 "rich_text": [{
                     "type": "text",
                     "text": {
                         "content": "这个是大标题",
                     }
                 }],
                 "color": "default",
                 "is_toggleable": False
             }
         }

     ],

     "icon": {
         "type": "external",
         "external": {
             "url": "https://www.biografiacortade.com/wp-content/uploads/2019/04/karl1-258x300.jpg"}
     },
     "cover": {
				"type": "external",
        "external": {
             "url": "https://www.biografiacortade.com/wp-content/uploads/2019/04/karl1-258x300.jpg"}}
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