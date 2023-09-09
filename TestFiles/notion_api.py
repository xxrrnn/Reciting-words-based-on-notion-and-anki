import requests

#基本参数
import configparser
config = configparser.ConfigParser()
config.read('../token.ini')
token = config.get('token', 'id')
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

def updata_page_properties(page_id,body,station):
    url = 'https://api.notion.com/v1/pages/'+page_id
    notion = requests.patch(url,headers=headers,json=body)

    if notion.status_code == 200:
        print(station+'·更新成功')
    else:
        print(station+'·更新失败')

    return 0

def get_page_information(page_id):
    url = 'https://api.notion.com/v1/pages/'+page_id
    notion_page = requests.get(url,headers=headers)
    result = notion_page.json()
    if notion_page.status_code == 200:
        print('页面属性获取成功')
    else:
        print('页面属性获取失败')

    return result

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


def DataBase_additem(database_id, body_properties, station):
    body = {
        'parent': {'type': 'database_id', 'database_id': database_id},
    }
    body.update(body_properties)

    url_notion_additem = 'https://api.notion.com/v1/pages'
    notion_additem = requests.post(url_notion_additem, headers=headers, json=body)

    if notion_additem.status_code == 200:
        print(station + '·更新成功')
    else:
        print(station + '·更新失败')

def pageid_information_pick(page_id,label):
    x = get_page_information(page_id)

    if label == 'id':
        output=x['id']
    else:
        type_x = x['properties'][label]['type']

        if type_x == 'checkbox':
            output = x['properties'][label]['checkbox']

        if type_x == 'date':
            output = x['properties'][label]['date']['start']

        if type_x == 'select':
            output = x['properties'][label]['select']['name']

        if type_x == 'rich_text':
            output = x['properties'][label]['rich_text'][0]['plain_text']

        if type_x == 'title':
            output = x['properties'][label]['title'][0]['plain_text']

        if type_x == 'number':
            output = x['properties'][label]['number']

    return output
def item_information_pick(item,label):
    x = item

    if label == 'id':
        output=x['id']
    else:
        type_x = x['properties'][label]['type']

        if type_x == 'checkbox':
            output = x['properties'][label]['checkbox']

        if type_x == 'date':
            output = x['properties'][label]['date']['start']

        if type_x == 'select':
            output = x['properties'][label]['select']['name']

        if type_x == 'rich_text':
            output = x['properties'][label]['rich_text'][0]['plain_text']

        if type_x == 'title':
            output = x['properties'][label]['title'][0]['plain_text']

        if type_x == 'number':
            output = x['properties'][label]['number']

    return output


def body_properties_input(body, label, type_x, data):
    if type_x == 'checkbox':
        body['properties'].update({label: {'type': 'checkbox', 'checkbox': data}})

    if type_x == 'date':
        body['properties'].update({label: {'type': 'date', 'date': {'start': data, 'end': None}}})

    if type_x == 'select':
        body['properties'].update({label: {'type': 'select', 'select': {'name': data}}})

    if type_x == 'rich_text':
        body['properties'].update(
            {label: {'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': data}, 'plain_text': data}]}})

    if type_x == 'title':
        body['properties'].update({label: {'id': 'title', 'type': 'title',
                                           'title': [{'type': 'text', 'text': {'content': data}, 'plain_text': data}]}})

    if type_x == 'number':
        body['properties'].update({label: {'type': 'number', 'number': data}})

    return body

def body_propertie_input(label, type_x, data):
    body = {
        'properties': {}
    }

    if type_x == 'checkbox':
        body['properties'].update({label: {'type': 'checkbox', 'checkbox': data}})

    if type_x == 'date':
        body['properties'].update({label: {'type': 'date', 'date': {'start': data, 'end': None}}})

    if type_x == 'select':
        body['properties'].update({label: {'type': 'select', 'select': {'name': data}}})

    if type_x == 'rich_text':
        body['properties'].update({label: {'type': 'rich_text', 'rich_text': [
            {'type': 'text', 'text': {'content': data}, 'plain_text': data}]}})

    if type_x == 'title':
        body['properties'].update({label: {'id': 'title', 'type': 'title',
                                           'title': [{'type': 'text', 'text': {'content': data}, 'plain_text': data}]}})

    if type_x == 'number':
        body['properties'].update({label: {'type': 'number', 'number': data}})

    return body

def select_items_form_Databaseid(Database_id,label,value):
    items = DataBase_item_query(Database_id)
    items_pick = []

    for item in items:
        if item_information_pick(item,label) == value:
            items_pick.append(item)

    return items_pick

def select_items_form_Databaseitems(items,label,value):
    items_pick = []

    for item in items:
        if item_information_pick(item,label) == value:
            items_pick.append(item)

    return items_pick

def find_duplicates(input_list):
    duplicates = []
    seen = set()

    for item in input_list:
        if item in seen:
            duplicates.append(item)
        else:
            seen.add(item)

    return duplicates


# https://www.notion.so/luminary-96bd5d554faf49aa9b02c702b76ecdfb?pvs=4
delete_page("96bd5d554faf49aa9b02c702b76ecdfb")




# https://www.notion.so/217a6cab505e4e52b85246a9610bb467?v=6bf2517c64914cc58902c8860808693b&pvs=4
# https://www.notion.so/yacht-f8b5a284368343758886f45ce107e947?pvs=4




get_page_information("f8b5a284368343758886f45ce107e947")



#test_word
# https://www.notion.so/179911edeb864a8fa464fa1caf7ec3da?v=d7ca612cf0f641cca59a3d9b6d4e6284&pvs=4
response = DataBase_item_query('94cc35f2d7ba46e0b9bdaecce97c116b')
import pickle
# with open('words_dict.data', 'wb') as file:
#     pickle.dump(response,file)
words = []
# with open('words_dict.data','rb') as file:
#     load_list = pickle.load(file)
# print(load_list)
count = 0
for dict in response:
        try:
            if dict['properties']['passage']['multi_select'][0]['name'] != -1:
                # print(dict['properties']['words']['title'][0]['plain_text'])
                words.append(dict['properties']['words']['title'][0]['plain_text'])
                count += 1
        except:
            print(dict)
            continue
print("count",count)
with open('TxtDataFiles/vocabularies.data', 'wb') as file:
    pickle.dump(words,file)
with open('TxtDataFiles/vocabularies.data','rb') as file:
    my_dict = pickle.load(file)

for dict_num in range(len(my_dict)):
    # if ' ' == self.my_dict[dict_num][0] or ' ' == self.my_dict[dict_num][len(self.my_dict[dict_num]) - 1]:
    my_dict[dict_num] = my_dict[dict_num].strip()
    my_dict[dict_num] = my_dict[dict_num].replace('\n', '')
    print(my_dict[dict_num])
with open('TxtDataFiles/vocabularies.data', 'wb') as file:
    pickle.dump(my_dict,file)

# print(vocabulary)
# print(vocabulary)
# print(len(vocabulary))