'''
全部代码位置
2023-8-15
version:1
目标：
anki 版本，修改上传的类型

问题：
只有英文翻译情况下，没有释义；暂时不改了，自己加上。也好加，使用is_chinese_soup来判断，再爬虫就是了
顺序上传notion中是反的，现在改成反向上传了
开始使用git来维护代码
'''

# import click
# import notion_api
# import notion_post
# import recognition_word
# import extract_epub

import numpy as np
import cv2
import pyautogui
# import paddleocr
from PIL import Image
import time
# import pywinauto.mouse
import ebooklib
from ebooklib import epub
from urllib import parse
import pyperclip
import requests
import re
from bs4 import BeautifulSoup
import subprocess
import pickle
import chardet
from datetime import timedelta, date
import datetime
import random
import configparser

class Economists:
    # 类属性（类级别的属性）
    # class_attribute = "This is a class attribute"
    # anki https://www.notion.so/4d044f4888104a4c89fbe30487f0198f?v=49f70ebd825a4c85a2a13b9ea10180b8&pvs=4
    # 构造函数（初始化方法）
    def __init__(self):
        # 实例属性（对象级别的属性）
        # self.title = None
        # self.DataBaseAPI = None
        # self.epub_path = "E:/TsinghuaCloud/Seafile/Economist/2023-3-11/TE-2023-03-11-EPUB.epub"
        config = configparser.ConfigParser()
        config.read('token.ini')
        self.token = config.get('token', 'id')
        self.database_id = config.get('database', 'anki_query')  # 取database前边的
        self.guidURL = 'https://dictionary.cambridge.org/dictionary/english-chinese-simplified/'
        self.guidURL_en = 'https://dictionary.cambridge.org/us/dictionary/english/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        self.notion_headers = {
            "Authorization": "Bearer " + self.token,
            "accept": "application/json",
            "Notion-Version": "2022-06-28"  # Notion版本号
        }


        self.words = []
        self.words_origin = []
        self.sentences = []
        self.num = "060"
        self.my_dict = []

    def find_middle_sentence_with_phrase(sentence_list, target_phrase):
        # 将目标词组转换为小写，以忽略大小写的差异
        target_phrase = target_phrase.lower()

        # 遍历句子列表，找到特定词组在句子中的索引位置
        matching_indices = [index for index, sentence in enumerate(sentence_list) if target_phrase in sentence.lower()]

        # 找到中间句子的索引位置
        middle_index = len(sentence_list) // 2

        # 遍历找到的索引位置，找到离中间位置最近的索引
        closest_index = min(matching_indices, key=lambda x: abs(x - middle_index))

        # 返回中间句子的索引位置和句子内容
        return sentence_list[closest_index]

    def next_day_on_level(self, level):
        if level == '0':
            n = 1
        elif level == '1':
            n = 2
        elif level == '2':
            n = 2
        elif level == '3':
            # n = 3
            n = int(random.randint(3, 5))
        elif level == '4':
            # n = 8
            n = int(random.randint(6, 9))
        elif level == '5':
            # n = 15
            n = int(random.randint(13, 17))
        elif level == '6':
            # n = 30
            n = int(random.randint(28, 32))
        elif level == '7':
            # n = 60
            n = int(random.randint(55, 60))
        elif level == '8':
            # n = 90
            n = int(random.randint(58, 93))
        elif level == '9':
            n = 120
        else:
            n = 1
            print("wrong level")
        return (date.today() + timedelta(days=n)).strftime('%Y-%m-%d')
    def setup(self):
        # 关闭clash代理
        print("开始关闭clash，请不要动鼠标。")
        notion_position = pyautogui.locateOnScreen('pictures/clash.png', grayscale=True, confidence= 0.9)
        notion_center = pyautogui.center(notion_position)
        pyautogui.click(notion_center, clicks=1, interval=0.25)
        time.sleep(3)
        notion_position = pyautogui.locateOnScreen('pictures/open.png', grayscale=True, confidence=0.9)
        if notion_position != None:
            notion_center = pyautogui.center(notion_position)
            pyautogui.click(notion_center, clicks=1, interval=0.25)
        time.sleep(1)
        clash_position = pyautogui.locateOnScreen('pictures/clash.png', grayscale=True, confidence=0.9)
        clash_center = pyautogui.center(clash_position)
        pyautogui.click(clash_center, clicks=1, interval=0.25)
        time.sleep(1)
        # pycharm_position = pyautogui.locateOnScreen('pycharm.png', grayscale=True, confidence=0.9)
        # pycharm_center = pyautogui.center(pycharm_position)
        # pyautogui.click(pycharm_center, clicks=1, interval=0.25)
        pass
    # to do
    # def get_today(self):
    #
    #     # 获取当前日期
    #     current_date = datetime.now().date()
    #
    #     # 将日期格式化为 "YYYY-MM-DD" 形式
    #     formatted_date = current_date.strftime('%Y-%m-%d')
    #     return formatted_date
    def get_cambridge_soup(self,word_to_search):
        current_guideUrl = self.guidURL
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        url = current_guideUrl + word_to_search
        source_code = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(source_code, 'html.parser')
        is_chinese_soup = True
        if len(soup.find_all(class_='def ddef_d db')) != 0:
            return soup,is_chinese_soup
        else:
            is_chinese_soup = False
            current_guideUrl = self.guidURL_en
            url = current_guideUrl + word_to_search
            source_code = requests.get(url, headers=self.headers).text
            soup = BeautifulSoup(source_code, 'html.parser')
            if len(soup.find_all(class_='def ddef_d db')) == 0:
                return [] ,is_chinese_soup
            else:
                return soup ,is_chinese_soup

    def get_cambridge_translation(self, soup, word, is_chinese_soup):
        if len(soup) == 0:
            return [], []
        all = []
        # with open("soup_interest.txt",'w') as file:
        #     file.write(str(soup.prettify()))
        #     file.close()

        # print(soup.prettify())
        # 判断是否有>的，比如 vested interests 和 credit
        # phrase-title dphrase-title 可以找到具体的词组英文
        # phrase-body dphrase_b 或  pr phrase-block dphrase-block 可以中英文释义
        # 得到这个，与后面得到的对比去重，得到最终的结果
        phrase = []
        # phrase_title = []
        phrase_translation = []
        phrase_chinese = []
        phrase_english = []
        translation = []

        # pr phrase-block dphrase-block
        if is_chinese_soup:
            phrase_all_span = soup.find_all(
                class_=['pr phrase-block dphrase-block', 'pr phrase-block dphrase-block lmb-25'])
            # print(phrase_all_span)
            if phrase_all_span != None:
                count = 0
                for phrase_all_span in phrase_all_span:
                    current_phase = []
                    count += 1
                    # print(phrase_all_span)
                    # print("+++++++++++++++++++++++++++++++++++++++")
                    phrase_title_span = phrase_all_span.find_all(class_=['phrase-title dphrase-title'])
                    pattern = r'>(.*?)<'
                    phrase_titles_span = re.findall(pattern, str(phrase_title_span))
                    phrase_title = ""
                    # ['', 'and so on', '']
                    for i in phrase_titles_span:
                        # if word in i:
                        #     current_phase.append(i)
                        #     break
                        phrase_title += i
                    print(phrase_title)
                    current_phase.append(phrase_title)
                    # 下面开始找释义 先英文后中文
                    eng = []
                    chi = []
                    phrase_engs_span = phrase_all_span.find_all(class_=['def ddef_d db'])
                    # print("phrase_engs_span",phrase_engs_span)
                    for phrase_eng_span in phrase_engs_span:
                        pattern = r'>(.*?)<'
                        english_span = re.findall(pattern, str(phrase_eng_span))
                        english_span = ''.join(english_span)
                        if english_span not in phrase_english:
                            eng.append(english_span)
                            phrase_english.append(english_span)
                    # print("eng",eng)

                    chinese_spans = phrase_all_span.find_all(class_='trans dtrans dtrans-se break-cj')
                    # [<span class="trans dtrans dtrans-se break-cj" lang="zh-Hans">是…的骄傲;是…的光荣</span>]
                    for chinese_span in chinese_spans:
                        if chinese_span.string not in phrase_chinese:
                            chinese_span_string = chinese_span.string
                            chinese_span_string = chinese_span_string.replace(';','；')
                            chi.append(chinese_span_string)
                            phrase_chinese.append(chinese_span_string)
                    # print("chi",chi)
                    if len(eng) == len(chi):
                        # for i in range(len(chi)):
                        #     current_phase.append(eng[i])
                        #     current_phase.append(chi[i])
                        current_phase.append(eng)
                        current_phase.append(chi)
                    else:
                        print(eng)
                        print(chi)
                        print("出现错误，debug！")
                    # print(current_phase)
                    # ['and all', ['and everything else', 'too'], ['以及其他一切；等等', '也']]
                    phrase.append(current_phase)
            # print(phrase)

            # 需要检测>，需要区分每个释义才能完成
            # phrase_spans = soup.find_all(class_='phrase-body dphrase_b')
            # for phrase_span in phrase_spans:
            #     print(phrase_span)
            # phrase.append(phrase_span.string)

            # 爬虫全部中文释义
            chinese_spans = soup.find_all(class_='trans dtrans dtrans-se break-cj')
            # print(chinese_spans)
            chinese = []
            for chinese_span in chinese_spans:
                chinese_span = chinese_span.string
                chinese_span = chinese_span.replace(';','；')
                chinese.append(chinese_span)
            # 爬虫全部英文释义
            english_spans = soup.find_all(class_='def ddef_d db')
            english = []
            for english_span in english_spans:
                pattern = r'>(.*?)<'
                english_span = re.findall(pattern, str(english_span))
                english_span = ''.join(english_span)
                english.append(english_span)
                # all[i].append(english)
            if len(chinese) == len(english):
                # for i in range(len(chinese)):
                #     one_translation = []
                #     one_translation.append(word)
                #     one_translation.append(english[i])
                #     one_translation.append(chinese[i])
                #     translation.append(one_translation)
                translation.append(word)
                translation.append(english)
                translation.append(chinese)
            else:
                print(word)
                print("chinese_num != english_num，中英文释义不对应，debug！")
            # all_translation_en = [row[1] for row in translation]
            # print(all_translation_en)
            for one_phrase_english in phrase_english:
                if one_phrase_english in english:
                    i = english.index(one_phrase_english)
                    translation[1].pop(i)
                    translation[2].pop(i)

            print("translation",translation)
            print("phrase",phrase)
            # 最终结果是translation 和 phrase translation，如果没有phrase，后者就是空的
            return translation, phrase
        else:
            translation.append(word)
            translation.append("")
            translation.append("")
            return translation, phrase
    def get_cambridge_origin_pronoun_voice(self,soup, flag = 1):
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
        # print(pronounciation)

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
        pass
        # return translation, phrase_translation

    # 实例方法
    def notion_scrap(self): # 词组和单词区分的任务难以完成，改用调用剪切版的方式获得单词信息
        print("开始执行")
        time.sleep(5)
        pos = []
        scores = []
        while(True):
            #截屏并读取
            im1 = pyautogui.screenshot('pictures/my_screenshot.png')
            img = cv2.imread("pictures/my_screenshot.png")
            # 转到HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # 设置阈值
            # l_blue = np.array([[0, 43, 46]])
            # h_blue = np.array([25, 255, 255])

            l_blue = np.array([5, 50, 50])  # 橙色的下限
            h_blue = np.array([15, 255, 255])  # 橙色的上限
            # 构建掩模
            mask = cv2.inRange(hsv, l_blue, h_blue)
            # 进行位运算
            res = cv2.bitwise_and(img, img, mask=mask)
            cv2.imwrite("pictures/result.png", res)
            # 开始ocr
            # 模型路径下必须含有model和params文件，如果没有，现在可以自动下载了，不过是最简单的模型
            # use_gpu 如果paddle是GPU版本请设置为 True
            ocr = paddleocr.PaddleOCR(use_angle_cls=True, use_gpu=False)
            img_path = "pictures/result.png"  # 这个是自己的图片，自行放置在代码目录下修改名称
            result = ocr.ocr(img_path, cls=True)

            img_res = cv2.imread("pictures/result.png")
            height_img, width_img, _ = img_res.shape
            # print(height_img, width_img)
            for lines in result:
                for line in lines:
                    print("pos", line[0])
                    pos.append(line[0])
                    print("word + scores", line[1])
                    #要解决词组识别率比单词低的情况
                    if ' ' in line[1][0]:
                        if line[1][1] >= 0.93:
                            self.words.append(line[1][0])
                    else:
                        if line[1][1] >= 0.93:
                            self.words.append(line[1][0])

                    # scores.append(line[1][1])
            #获得了word,再次截屏，如果变化没超过阈值，就认为
            if 'This article was downloaded' in self.words:
                new_words = list(filter(lambda x: x != 'This article was downloaded', self.words))
                # print(new_words)
                # print("new_words",len(new_words),new_words)

                # 处理识别出空格的单词
                for num in range(len(new_words)):
                    new_words[num] = new_words[num].strip()
                self.words = list(set(new_words))
                print("words",len(self.words),self.words)
                # cv2.imshow("res",img_res)
                # cv2.waitKey()
                break
            pyautogui.click(800,800, clicks=1, interval=0.25)
            pywinauto.mouse.scroll((800,300),-2) #(1100,300)是初始坐标，1000是滑动距离（可负）
        return self.words
        pass
    def new_dict(self):
        url_notion_block = 'https://api.notion.com/v1/databases/' + self.database_id + '/query'
        res_notion = requests.post(url_notion_block, headers=self.notion_headers)
        S_0 = res_notion.json()
        res_travel = S_0['results']
        if_continue = len(res_travel)
        if if_continue > 0:
            while if_continue % 100 == 0:
                body = {
                    'start_cursor': res_travel[-1]['id']
                }
                res_notion_plus = requests.post(url_notion_block, headers=self.notion_headers, json=body)
                S_0plus = res_notion_plus.json()
                res_travel_plus = S_0plus['results']
                for i in res_travel_plus:
                    if i['id'] == res_travel[-1]['id']:
                        continue
                    res_travel.append(i)
                if_continue = len(res_travel_plus)
        words = []
        count = 0
        for dict in res_travel:
            try:
                if dict['properties']['passage']['multi_select'][0]['name'] != -1:
                    # print(dict['properties']['words']['title'][0]['plain_text'])
                    words.append(dict['properties']['words']['title'][0]['plain_text'])
                    count += 1
            except:
                print(dict)
                continue
        print("count", count)
        # with open('vocabularies.data', 'wb') as file:
        #     pickle.dump(words, file)
        # with open('vocabularies.data', 'rb') as file:
        #     my_dict = pickle.load(file)

        for dict_num in range(len(words)):
            # if ' ' == self.my_dict[dict_num][0] or ' ' == self.my_dict[dict_num][len(self.my_dict[dict_num]) - 1]:
            words[dict_num] = words[dict_num].strip()
            words[dict_num] = words[dict_num].replace('\n', '')
            print(words[dict_num])
        with open('vocabularies.data', 'wb') as file:
            pickle.dump(words, file)

    def get_words_txt(self):

        with open("words.txt", "rb") as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)

        # 使用检测到的编码来打开文件
        self.detected_encoding = result["encoding"]
        # with open("filename.txt", "r", encoding=detected_encoding) as file:



        # with open("words.txt", "r", encoding="utf-8") as file:
        with open("words.txt", "r", encoding=self.detected_encoding) as file:
            words = file.readlines()
        for num in range(len(words)):
            words[num] = words[num].replace('\n','')
        for word in words:
            if word not in self.words and len(word) != 0:
                self.words.append(word)

    def get_clip_passage(self):
        pyperclip.copy('')
        # 初始上一次的剪切板内容为空
        prev_clipboard_content = ''
        with open("passage.txt", 'w', encoding='utf-8') as file:
            file.truncate()
        print("检查clash是否关闭")
        input("文档已经清空，请选中并复制全部文章，enter开始运行")
        while True:
            # 获取剪切板内容
            # time.sleep(5)
            clipboard_content = pyperclip.paste()
            clipboard_content = clipboard_content.strip()
            # # 如果剪切板内容发生变化且不为空，则写入到txt文件中
            # if clipboard_content != prev_clipboard_content and clipboard_content and clipboard_content not in self.words:
            print(clipboard_content)
            # with open("all_passage.txt", 'r', encoding='utf-8') as file:
            #     file.write(clipboard_content)
            with open("passage.txt", 'w', encoding='utf-8') as file:
                file.write(clipboard_content)
            # self.words.append(clipboard_content)
            # 更新上一次的剪切板内容为当前内容
            # prev_clipboard_content = clipboard_content
            resp = input("文章全部复制了？ 1/0")
            if resp != "0":
                break
            # 每隔一秒钟检查一次剪切板内容
            time.sleep(1)
        subprocess.run(['notepad.exe', "passage.txt"], check=True)

    def get_clip(self):
        pyperclip.copy('')
        # 初始上一次的剪切板内容为空
        prev_clipboard_content = ''
        with open("words.txt", 'w',encoding='utf-8') as file:
            file.truncate()
        print("检查clash是否关闭")
        print("文档已经清空，开始运行，可以开始选词")

        while True:
            # 获取剪切板内容
            clipboard_content = pyperclip.paste()
            clipboard_content = clipboard_content.strip()
            if clipboard_content == "20":
                print("停止检测单词")
                break
            # 如果剪切板内容发生变化且不为空，则写入到txt文件中
            if clipboard_content != prev_clipboard_content and clipboard_content and clipboard_content not in self.words:
                with open("words.txt", 'a',encoding='utf-8') as file:
                    file.write(clipboard_content + '\n')
                    print(clipboard_content)
                    # self.words.append(clipboard_content)
                # 更新上一次的剪切板内容为当前内容
                prev_clipboard_content = clipboard_content

            # 每隔一秒钟检查一次剪切板内容
            time.sleep(1)
        subprocess.run(['notepad.exe',"words.txt"],check = True)
        # myinput = input("完成剪切板调用，请检查文档内容并修正")
        with open("words.txt","r") as file:
            words_txt = file.readlines()
        for word in words_txt:
            word = word.replace('\n','')
            if word not in self.words and len(word) != 0:
                self.words.append(word)
        with open("words.txt", "rb") as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)

        # 使用检测到的编码来打开文件
        self.detected_encoding = result["encoding"]




    def get_sentences(self):
        # with open("words.txt","r",encoding='utf-8') as file:
        #     words = file.readlines()
        # words = [item.replace('\n', '') for item in words]
        # self.words = words

        # with open("passage.txt", "r", encoding='utf-8') as bookFile:
        #     paragraphs = bookFile.readlines()


        # copy notion to txt, use this
        with open("passage.txt", "rb") as file:
            lines = file.readlines()

        paragraphs = []

        for line in lines:
            try:
                paragraph = line.decode('utf-8')  # 尝试用utf-8解码
                paragraphs.append(paragraph)
            except UnicodeDecodeError:
                # 如果utf-8解码失败，则使用latin-1解码
                paragraph = line.decode('latin-1', errors='replace')  # 替换无法解码的字符
                paragraphs.append(paragraph)
        #分句
        sentences_all = []
        for paragraph in paragraphs:
            dot_index = [0]
            paragraph = paragraph.replace("\r\n","")
            if "." not in paragraph or " " not in paragraph:
                if len(paragraph) != 0:
                    sentences_all.append(paragraph)
                    continue
            for alpha_num in range(len(paragraph)):
                if alpha_num != 0:
                    if paragraph[alpha_num-1] == "." and paragraph[alpha_num] == " ":
                        dot_index.append(alpha_num)
                    elif paragraph[alpha_num-2] == "." and paragraph[alpha_num-1] == ")":
                        dot_index.append(alpha_num)
                    elif paragraph[alpha_num-2] == "." and paragraph[alpha_num-1] == "\"":
                        dot_index.append(alpha_num)
                    else:
                        pass
            for dot_num in range(len(dot_index)-1):
                sentences_all.append(paragraph[dot_index[dot_num]:dot_index[dot_num + 1]])



            # 去除* 和 # 和 (http)
        for sen_num in range(len(sentences_all)):
            sentence = sentences_all[sen_num]
            if "long-planned" in sentences_all[sen_num] :
                pass
            sentences_all[sen_num] = sentences_all[sen_num].replace('\n', '')
            sentences_all[sen_num] = sentences_all[sen_num].replace('\r', '')
            sentences_all[sen_num] = sentences_all[sen_num].strip('*# ')
            sentences_all[sen_num] = re.sub(r'\((.*?)\)|\[([^\]]+)\]', lambda m: m.group(2) if m.group(2) else "", sentences_all[sen_num] )
            # sentences_all[sen_num] = sentences_all[sen_num].strip('*')
            # sentences_all[sen_num] = sentences_all[sen_num].strip()
            # sentences_all[sen_num] = sentences_all[sen_num].strip('#')
            # sentences_all[sen_num] = sentences_all[sen_num].strip()
            # sentences_all[sen_num] = sentences_all[sen_num].strip('*')
            # sentences_all[sen_num] = sentences_all[sen_num].strip()
            a = sentences_all[sen_num]
        for word_num in range(len(self.words)):
            find_true_sentence = False
            current_word = self.words[word_num]
            sentences_contain_word = []
            # if "main" in current_word:
            #     print("main")
            if ' ' in current_word or '-' in current_word: # 词组
                for sentence in sentences_all:
                        if self.words[word_num] in sentence:
                            sentences_contain_word.append(sentence)
                            find_true_sentence = True
                            break

                                # if '\n' in sentence:
                                #     sentence = sentence.replace('\n', '')
                                # if '.' in sentence:
                                #     self.sentences.append(sentence)
                                # else:
                                #     self.sentences.append(sentence + '.')
            else:   #单词，因为有的单词是被其他单词包含的，需要分割为list才能用in
                for paragraph in paragraphs:
                    if find_true_sentence:
                        break
                    for sentence in sentences_all:
                        if current_word in sentence:
                            if self.words[word_num] in sentence:
                                # print(self.words[word_num] , sentence)
                                if self.words[word_num] in sentence.split(' '):
                                    sentences_contain_word.append(sentence)
                                    find_true_sentence = True
                                    break
                                elif self.words[word_num] in sentence.split('-'):
                                        sentences_contain_word.append(sentence)
                                        find_true_sentence = True
                                        break
                                else:
                                    # print(self.words[word_num])
                                    # print(sentence)
                                    sentences_contain_word.append(sentence)



            for sentence_contain_word in sentences_contain_word:
                if '\n' in sentence_contain_word:
                    sentence_contain_word = sentence_contain_word.replace('\n', '')
                if '\r' in sentence_contain_word:
                    sentence_contain_word = sentence_contain_word.replace('\r', '')
                if '.' not in sentence_contain_word:
                    sentence_contain_word += '.'
            self.sentences.append(sentence_contain_word)
                        # print(self.words[word_num])
                        # print(len(self.sentences))
        # for num in len(self.sentences):
        #     print(self.words[num],self.sentences[num])

    def get_cambridge(self):
        translations = []
        error_words = []
        origin_pronoun_voice = []
        for word in self.words:
            current_soup, is_chinese_soup = self.get_cambridge_soup(word)
            origin, pronounciation, voice = self.get_cambridge_origin_pronoun_voice(current_soup)
            self.words_origin.append(origin)
            # print(origin,pronounciation)
            translation, phase_translation = self.get_cambridge_translation(current_soup,word,is_chinese_soup)
            # print(translation,phase_translation)

            if origin == None or pronounciation == None or translation == None:
                error_words.append(word)
                continue
            ori_pro_voi = []
            current_translations = []
            ori_pro_voi.append(origin)
            ori_pro_voi.append(pronounciation)
            ori_pro_voi.append(voice)
            origin_pronoun_voice.append(ori_pro_voi)
            current_translations.append(word)
            current_translations.append(ori_pro_voi)
            current_translations.append(translation)
            current_translations.append(phase_translation)
            translations.append(current_translations)
        # for i in translations:
        #     print(i)
        # print(origin_pronoun, error_words)
        print("translations",translations)
        return origin_pronoun_voice,translations, error_words

    def notion_post(self, word_tag,word_color,word_content,meaning,pronoun,sentence,voice_url):
        today_str = date.today().strftime('%Y-%m-%d')
        next_str = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        url = "https://api.notion.com/v1/pages"
        p = {"parent": {"database_id": self.database_id},
             "properties": {
                 "Tags": {"select": {"name": word_tag, "color": word_color}},
                 "words": {"title": [{"type": "text", "text": {"content": word_content}}]},
                 "passage": {"multi_select": [{"name": self.num}]},
                 "phonetic symbol": {"rich_text": [{"type": "text", "text": {"content": pronoun}}]},
                 "meaning": {
                     "rich_text": [{"type": "text", "text": {"content": meaning}}]},
                 "Last": {"date": {"start": today_str}},
                 "Next": {"date": {"start": next_str}},
                 "voice": {"url": voice_url},
                 "Level": {"select": {"name": "0", "color": "default"}},
                 "KnowAll": {"checkbox": False},
                 "KnowSome": {"checkbox": False},
                 "ForgetAll": {"checkbox": False},


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
                                 "content": sentence,
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
            "Authorization": "Bearer " + self.token
        }
        r = requests.post(url, json=p, headers=headers)
        print(r.text)
        if r.status_code == 200:
            print("导入Notion成功！" + word_content)
        else:
            print("导入Notion失败！")

    def run(self):
        try:
            source_code = requests.get(self.guidURL + 'and', headers=self.headers).text
        except:
            self.setup()
        self.num = input("输入这次的文章标号：参考063：\n")
        selection = input("passage.txt是否已经是本次文章了,不是打0 \n")
        if selection == "0":
            self.get_clip_passage()
        else:
            pass
        selection = input("words.txt是否已经是拷贝的单词,是打1,不是打0 \n")
        if selection == "1":
            self.get_words_txt()
        else:
            self.get_clip()
        print(len(self.words),self.words)
        input("check it \n")
        self.get_sentences()
        origin_pronoun_voice,translations, error_words = self.get_cambridge()
        if len(self.words) != len(self.sentences):
            print("word",len(self.words),"sentences",len(self.sentences))
            print("单词和例句数量不对应，debug！")
            return None
        print(len(self.words),len(self.sentences))
        with open("words.txt", 'w',encoding=self.detected_encoding) as file:
            file.truncate()
            for w in self.words:
                file.write(w + "\n")
        with open("words_upload.txt", 'w',encoding=self.detected_encoding) as file:
            file.truncate()
        with open("words_repeat.txt", 'w',encoding=self.detected_encoding) as file:
            file.truncate()

        print("word",self.words)
        print("sentences",self.sentences)
        print("error",error_words)
        is_check = input("要不要检查有没有重复 1/0: \n")
        if is_check == "1":
            with open('vocabularies.data', 'rb') as file:
                self.my_dict = pickle.load(file)
        else:
            pass
        print(self.my_dict)
        print(len(self.my_dict))
        for dict_num  in range(len(self.my_dict)):
            # if ' ' == self.my_dict[dict_num][0] or ' ' == self.my_dict[dict_num][len(self.my_dict[dict_num]) - 1]:
            self.my_dict[dict_num] = self.my_dict[dict_num].strip()
            self.my_dict[dict_num] = self.my_dict[dict_num].replace('\n','')
            pass

        translations_num = 0
        chongfu_num = 0
        up_word_tag = []
        up_word_color = []
        up_word_content = []
        up_meaning = []
        up_pronoun = []
        up_sentence = []
        up_voiceUrl = []
        print(self.my_dict)

        for i in range(len(self.words)):
            current_word = self.words[i]
            if self.words[i] not in error_words:
                if self.words[i] in self.my_dict or self.words_origin[i] in self.my_dict:
                    chongfu_num += 1
                    with open("words_repeat.txt","a", encoding='utf-8') as file:
                        current_translation = translations[translations_num]
                        # except:
                        # print(self.words[i])
                        file.write("-------------------- word " + str(i) + " --------------------" + "\n")
                        word_in_passage = current_translation[0]
                        file.write(word_in_passage + "\n")
                        word_origin = current_translation[1][0]
                        file.write(word_origin + "\n")
                        word_pronoun = current_translation[1][1]
                        # file.write(word_pronoun + "\n")
                        voiceUrl = current_translation[1][2]
                        file.write(voiceUrl + "\n")
                        eng_trans = current_translation[2][1]
                        chi_trans = current_translation[2][2]

                        file.write("===== translation" + str(i) + " =====" + "\n")
                        for j in range(len(chi_trans)):
                            file.write(eng_trans[j] + " \n")
                            file.write(chi_trans[j] + " \n")
                        file.write(">>>>> phrase " + str(i) + " <<<<<" + "\n")
                        phrase_all = current_translation[3]
                        if len(phrase_all) != 0:
                            for current_phrase in phrase_all:
                                phrase_word = current_phrase[0]
                                phrase_eng_trans = current_phrase[1]
                                phrase_chi_trans = current_phrase[2]
                                file.write(phrase_word + "\n")
                                for pj in range(len(phrase_chi_trans)):
                                    file.write(phrase_eng_trans[pj] + "\n")
                                    file.write(phrase_chi_trans[pj] + "\n")
                            pass
                        file.write("///// sentences " + str(i) + " /////" + "\n")
                        file.write(self.sentences[i] + "\n")
                    translations_num += 1
                    continue
                else:
            # if self.words[i] not in error_words:
                    with open("words_upload.txt","a",encoding='utf-8') as file:
                        # file.write(self.words[i] + " " + origin_pronoun + "\n")
                        # file.write(translations[i] + "\n")
                        # file.write(self.sentences[i] + "\n")
                        # print(self.words[i] + " " + origin_pronoun + "\n")
                        # print(translations[i] + "\n")
                        # try:
                        current_translation = translations[translations_num]
                        # except:
                        # print(self.words[i])
                        file.write("-------------------- word "+ str(i)+" --------------------"+ "\n")
                        word_in_passage = current_translation[0]
                        file.write(word_in_passage + "\n")
                        word_origin = current_translation[1][0]
                        file.write(word_origin + "\n")
                        up_word_content.append(word_origin)
                        word_pronoun = current_translation[1][1]
                        voiceUrl = current_translation[1][2]
                        up_pronoun.append(word_pronoun)
                        print("voiceUrl",voiceUrl)
                        up_voiceUrl.append(voiceUrl)
                        # file.write(word_pronoun + "\n")
                        try:
                            eng_trans = current_translation[2][1]
                            chi_trans = current_translation[2][2]
                        except:
                            eng_trans = ""
                            chi_trans = ""

                        file.write("===== translation" + str(i) +" ====="+ "\n")
                        meaning = ""
                        for j in range(len(chi_trans)):
                            file.write(eng_trans[j]+ " \n")
                            file.write(chi_trans[j]+ " \n")
                            meaning += eng_trans[j]+ " \n"
                            meaning += chi_trans[j]+ " \n"
                        file.write(">>>>> phrase " + str(i) + " <<<<<" + "\n")
                        phrase_all = current_translation[3]
                        if len(phrase_all) != 0:
                            meaning += "-----phrase-----\n"
                            for current_phrase in phrase_all:
                                phrase_word = current_phrase[0]
                                phrase_eng_trans = current_phrase[1]
                                try:
                                    phrase_chi_trans = current_phrase[2]
                                except:
                                    phrase_chi_trans = ""
                                file.write(phrase_word + "\n")
                                meaning += phrase_word + "\n"
                                for pj in range(len(phrase_chi_trans)):
                                    file.write(phrase_eng_trans[pj] + "\n")
                                    file.write(phrase_chi_trans[pj] + "\n")
                                    meaning +=phrase_eng_trans[pj] + "\n"
                                    meaning +=phrase_chi_trans[pj] + "\n"
                            pass
                        up_meaning.append(meaning)
                        file.write("///// sentences " + str(i) + " /////" + "\n")
                        file.write(self.sentences[i] + "\n")
                        up_sentence.append(self.sentences[i])
                    translations_num += 1
            else:
                if self.words[i] in self.my_dict:
                    chongfu_num += 1
                    with open("words_repeat.txt","a",encoding='utf-8') as file:
                        file.write("-------------------- error word " + str(i) + " --------------------" + "\n")
                        file.write(self.words[i] + "\n")
                        file.write("///// sentences " + str(i) + " /////" + "\n")
                        file.write(self.sentences[i] + "\n")
                else:
                    up_word_content.append(self.words[i])
                    with open("words_upload.txt","a",encoding='utf-8') as file:
                        file.write("-------------------- error word " + str(i) + " --------------------" + "\n")
                        file.write(self.words[i] + "\n")
                        file.write("///// sentences " + str(i) + " /////" + "\n")
                        file.write(self.sentences[i] + "\n")
                        up_sentence.append(self.sentences[i])
                        up_pronoun.append(" ")
                        up_meaning.append(" ")
                        up_voiceUrl.append(" ")

        if chongfu_num + len(up_meaning) == len(self.words):
            input("都对应上了，可以enter")
        subprocess.run(['notepad.exe',"words_upload.txt"],check = True)
        subprocess.run(['notepad.exe',"words_repeat.txt"],check = True)
        # input("检查result.txt，如果没有问题就enter")
        # 设置tag color
        for content_num in range(len(up_word_content)):
            up_word_content[content_num] = up_word_content[content_num].strip()
            if " " in up_word_content[content_num]:
                up_word_tag.append("词组")
                up_word_color.append("pink")
            else:
                up_word_tag.append("单词")
                up_word_color.append("yellow")
        print(len(up_meaning))
        print(len(up_pronoun))
        print(len(up_word_content))
        print(len(up_word_tag))
        print(len(up_word_color))
        print(len(up_voiceUrl))
        if len(up_voiceUrl) != len(up_word_content):
            for opv in origin_pronoun_voice:
                print(opv)
        # today = self.get_today()
        # today = self.get_today()
        # 开始上传notion
        for num in range(len(up_word_content)-1,-1,-1):
            self.notion_post(up_word_tag[num],up_word_color[num],up_word_content[num],up_meaning[num],up_pronoun[num],up_sentence[num],up_voiceUrl[num])
        # for word in self.words:
        #     if word not in self.my_dict:
        #         self.my_dict.append(word)
        self.new_dict()
        # with open('vocabularies.data', 'wb') as file:
        #     pickle.dump(self.my_dict, file)
    # for word in self.words:
        #     con = True
        #     for sen in self.sentences:
        #         if word in sen:
        #             con = False
        #             break
        #     if con:
        #         print(word)
        # page = cv2.imread("result.png")
        # cv2.imshow("page",page)
        # cv2.waitKey()

if __name__ == "__main__":
    test = Economists()
    # with open('vocabularies.data', 'rb') as file:
    #     my_dict = pickle.load(file)
    # print(my_dict)
    # soup = test.get_cambridge_soup("suasion")
    # test.get_cambridge_origin_pronoun_voice(soup)
    # test.notion()
    # print(len(test.notion()),)
    # test.get_sentences()
    test.run()

# with open("result.txt", "r") as file:
#     all_content = file.readlines()
#     word_index = []
#     for num in range(len(all_content)):
#         if "--------------------" in all_content[num]:
#             word_index.append[num]
#     for index in word_index:

    print("End")
