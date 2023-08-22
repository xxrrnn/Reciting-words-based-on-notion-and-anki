import requests
import re
from bs4 import BeautifulSoup
import random
from datetime import timedelta, date

# short https://www.notion.so/58951b5a29544562a93fd0c1f5d7112f?v=316bed45c314462c84dca09b30578cea&pvs=4
# query_id = "58951b5a29544562a93fd0c1f5d7112f"
# database_id = "316bed45c314462c84dca09b30578cea"
# https://www.notion.so/4d044f4888104a4c89fbe30487f0198f?v=49f70ebd825a4c85a2a13b9ea10180b8&pvs=4
query_id = "4d044f4888104a4c89fbe30487f0198f"
database_id = "49f70ebd825a4c85a2a13b9ea10180b8"
guidURL = 'https://dictionary.cambridge.org/dictionary/english-chinese-simplified/'
guidURL_en = 'https://dictionary.cambridge.org/us/dictionary/english/'
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

def get_cambridge_soup(word_to_search):
    current_guideUrl = guidURL
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    url = current_guideUrl + word_to_search
    source_code = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source_code, 'html.parser')
    is_chinese_soup = True
    if len(soup.find_all(class_='def ddef_d db')) != 0:
        return soup,is_chinese_soup
    else:
        is_chinese_soup = False
        current_guideUrl = guidURL_en
        url = current_guideUrl + word_to_search
        source_code = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source_code, 'html.parser')
        if len(soup.find_all(class_='def ddef_d db')) == 0:
            return [],is_chinese_soup
        else:
            return soup,is_chinese_soup

def get_cambridge_origin_pronoun_voice(soup, flag = 1):
    if len(soup) == 0:
        return None,None,None
    # 原词行获取
    #<span class="hw dhw">normalize</span>
    # origin_spans = soup.find_all(class_='hw dhw')
    origin_spans = soup.find_all(class_='tb ttn')
    if len(origin_spans) != 0:
        for origin_span in origin_spans:
            origin_pattern = r'>(.*?)<'
            origin = re.findall(origin_pattern, str(origin_spans))
            if origin != None:
                break
    else:
        return None,None,None
    # print(origin[0])

    # 音标获取
    # <span class="ipa dipa lpr-2 lpl-1">ˈnaɪ.sə.ti</span>
    # us_pronouns = soup.find_all(class_ = "i i-volume-up c_aud htc hdib hp hv-1 fon tcu tc-bd lmr-10 lpt-3 fs20 hv-3")#,title_ = "Escucha la pronunciación en inglés americano")
    pronoun_spans = soup.find_all(class_='ipa dipa lpr-2 lpl-1')
    # print(pronoun_spans)
    count = 0
    pronounciation = ""
    pronounciation_us = ""
    pronounciation_uk = ""
    for pronoun_span in pronoun_spans:
        pronoun_pattern = r'>(.*?)<'
        pronoun_gets = re.findall(pronoun_pattern, str(pronoun_span))
        res = ""
        for pronoun_get in pronoun_gets:
            if len(pronoun_get) == 0:
                continue
            res += pronoun_get
        count += 1
        if count == 1:
            pronounciation_uk += 'UK  /' + res + '/'
            pass
        else:
            pronounciation_us += '/' + res + '/'
        if len(pronounciation_us) != 0 and count == 2:
            break
    pronounciation = pronounciation_us
    if '//' in pronounciation or len(pronounciation) == 0:
        pronounciation = pronounciation_uk
    if '//' in pronounciation or len(pronounciation) == 0:
        pronounciation = ""
    print(pronounciation)
    # voice网址获取
    voice_spans = soup.find_all('source', type='audio/mpeg')
    # print("voice_up_spans",voice_up_spans)
    pattern = re.compile(r'src="([^"]+\.mp3)"')
    url_voice = ""
    for voice_span in voice_spans:
        match = pattern.search(str(voice_span))
        if match:
            extracted_voice = match.group(1)
            if "us_pron" in extracted_voice:
                url_voice = "https://dictionary.cambridge.org" + extracted_voice
                break
                pass
    # print(url_voice)
    return origin[0], pronounciation, url_voice


# def notion_words_patch(page_id,origin, pronoun, url_voice):
def notion_words_patch(page_id ,origin,pronounciation,url_voice):
    # print(level)
    colors = ["default","gray","brown","orange","yellow","green","blue","purple","pink","red"]
    data = {
        "parent": {"type": "database_id", "database_id": "49f70ebd825a4c85a2a13b9ea10180b8"},
        'properties': {
            # "Level": {"select": {"name": level, "color": colors[int(level)]}},
            # "words": {"title": [{"type": "text", "text": {"content": origin}}]},
            "phonetic symbol": {"rich_text": [{"type": "text", "text": {"content": pronounciation}}]},
            # "voice": {"url": url_voice},
            # "Date Wrong": {"date": {"start": "2023-11-21"}},
            # '移動方式': {'rich_text': [{"text": {"content": move}}]},
        }
    }
    r = requests.patch(
        "https://api.notion.com/v1/pages/{}".format(page_id),
        json=data,
        headers=headers,
    )
    print(r.text)

def patch_all_pronoun_and_voice(responce):
    all_page_id = []
    all_words = []
    count = 0
    for dict in response:
        all_page_id.append(dict['id'])
    for dict in response:
        try:
            if dict['properties']['passage']['multi_select'][0]['name'] != -1:
                # print(dict['properties']['words']['title'][0]['plain_text'])
                all_words.append(dict['properties']['words']['title'][0]['plain_text'])
                count += 1
        except:
            print(dict)
    for word_num in range(len(all_words)):
        word = all_words[word_num]
        page_id = all_page_id[word_num]
        print(word)
        print(word_num / count, count)
        soup,is_chinese = get_cambridge_soup(word)
        origin, pronounciation, url_voice = get_cambridge_origin_pronoun_voice(soup)
        if origin == None:
            origin = word
        if pronounciation == None:
            pronounciation = ""
        if url_voice == None:
            url_voice = ""
        notion_words_patch(page_id ,origin,pronounciation,url_voice)
    pass
def patch_all_level(responce):
    levels = []
    all_page_id = []
    count = 0
    for dict in response:
        all_page_id.append(dict['id'])
    for dict in response:
        con = True
        for num in range(6,0,-1):
            checkbox = 'Checkbox ' + str(num)
            if dict['properties'][checkbox]['checkbox'] == True:
                levels.append(str(num))
                count += 1
                con = False
                break
        if con:
            levels.append('0')

    print(levels)
    for num in range(len(all_page_id)):
        page_id = all_page_id[num]
        level = levels[num]
        notion_words_patch(page_id,level)




def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if (n < 0):
        n = abs(n)
        # formatted_date = current_date.strftime('%Y-%m-%d')
        return (date.today() - timedelta(days=n)).strftime('%Y-%m-%d')
    else:
        return (date.today() + timedelta(days=n)).strftime('%Y-%m-%d')

def patch_all_date(responce):
    dates = []
    all_page_id = []
    count = 0
    d_day = [0,1,2,3,4,5,6,7]
    for dict in response:
        all_page_id.append(dict['id'])
        count += 1
    for i in range(len(all_page_id)):
        day = random.sample(d_day, len(d_day))[0]
        dates.append(get_day_of_day(day))

    print(dates)
    for i in range(len(all_page_id)):
        print(i,i/count)
        date = dates[i]
        page_id = all_page_id[i]
        data = {
            "parent": {"type": "database_id", "database_id": database_id},
            'properties': {
                "Last": {"date": {"start": date}},
                # "Level": {"select": {"name": level, "color": colors[int(level)]}},
                # "words": {"title": [{"type": "text", "text": {"content": origin}}]},
                # "phonetic symbol": {"rich_text": [{"type": "text", "text": {"content": pronoun}}]},
                # "voice": {"url": url_voice},
                # "Date Wrong": {"date": {"start": "2023-11-21"}},
                # '移動方式': {'rich_text': [{"text": {"content": move}}]},
            }
        }
        r = requests.patch(
            "https://api.notion.com/v1/pages/{}".format(page_id),
            json=data,
            headers=headers,
        )
        print(r.text)



if __name__ == "__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read('../token.ini')
    token = config.get('token', 'id')

    headers = {
        "Authorization": "Bearer " + token,
        "accept": "application/json",
        "Notion-Version": "2022-06-28"  # Notion版本号
    }
    response = DataBase_item_query(query_id)
    patch_all_pronoun_and_voice(response)
    # patch_all_date(response)


