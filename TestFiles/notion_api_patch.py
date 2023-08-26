import requests
# https://www.notion.so/58951b5a29544562a93fd0c1f5d7112f?v=316bed45c314462c84dca09b30578cea&pvs=4

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


if __name__ == "__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read('../token.ini')
    token = config.get('token', 'id')
    query_id = config.get('database','anki_query')
    headers = {
        "Authorization": "Bearer " + token,
        "accept": "application/json",
        "Notion-Version": "2022-06-28"  # Notion版本号
    }
    all_page_id = []
    all_words = []
    response = DataBase_item_query(query_id)
    for dict in response:
        all_page_id.append(dict['id'])
        word = dict['properties']['words']['title'][0]['plain_text']
        word = word.strip()
        all_words.append(word)
    print(len(all_words),len(all_page_id))
    # page_id = "4ec6696bb3994c4fae2dc7e4ba6e192d"
    for num in range(len(all_page_id)):
        data = {
            "parent": {"type": "database_id", "database_id": query_id},
            'properties': {
                # "Level": {"select": {"name": level, "color": colors[int(level)]}},
                "words": {"title": [{"type": "text", "text": {"content": all_words[num]}}]},
                # "phonetic symbol": {"rich_text": [{"type": "text", "text": {"content": pronounciation}}]},
                # "voice": {"url": url_voice},
                # "Date Wrong": {"date": {"start": "2023-11-21"}},
                # '移動方式': {'rich_text': [{"text": {"content": move}}]},
            }
        }

        print(all_words[num])
        r = requests.patch(
            "https://api.notion.com/v1/pages/{}".format(all_page_id[num]),
            json = data,
            headers=headers,
        )
        print(r.text)