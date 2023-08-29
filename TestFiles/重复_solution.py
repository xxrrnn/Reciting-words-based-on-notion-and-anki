import configparser
import requests

config = configparser.ConfigParser()
config.read('../token.ini')
token = config.get('token', 'id')
database_id = config.get('database', 'anki_database')  # 取database前边的
query_id = config.get('database', 'anki_query')  # 取database前边的
headers = {
    "Authorization": "Bearer " + token,
    "accept": "application/json",
    "Notion-Version": "2022-06-28"  # Notion版本号
}
def find_duplicate_strings(input_list):
    seen = set()
    duplicates = set()

    for string in input_list:
        if string in seen:
            duplicates.add(string)
        else:
            seen.add(string)

    return list(duplicates)

def DataBase_item_query(query_database_id):
    # query_database_id = self.query_id
    url_notion_block = 'https://api.notion.com/v1/databases/'+query_database_id+'/query'
    res_notion = requests.post(url_notion_block,headers=headers)
    S_0 = res_notion.json()
    res_travel = S_0['results']
    if_continue = len(res_travel)
    print(len(res_travel))
    if if_continue > 0:
        while if_continue % 100 == 0:
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

def get_words_in_notion():
    response = DataBase_item_query(query_id)
    words = []
    for dict in response:
        words.append(dict['properties']['words']['title'][0]['plain_text'])

    return words


duplicate_strings = find_duplicate_strings(get_words_in_notion())
print(duplicate_strings)  # 输出：['banana', 'apple']
