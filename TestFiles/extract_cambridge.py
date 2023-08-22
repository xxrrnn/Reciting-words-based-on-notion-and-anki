import requests
import re
from bs4 import BeautifulSoup
# https://dictionary.cambridge.org/dictionary/english-chinese-simplified/rancorous
guidURL = 'https://dictionary.cambridge.org/dictionary/english-chinese-simplified/'
# guidURL = 'https://dictionary.cambridge.org/us/dictionary/english/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
guideURLs = []
extendURLs = []
def read_web(url, headers):
    # print(s)
    source_code = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source_code, 'html.parser')
    print(soup)
    return soup



def extract_web(url, headers, word,flag,num = 10,sentences = ""):
    #需要的元素有：英文、音标、英文中文释义，例句
    source_code = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source_code, 'html.parser')
    # all = [[j for j in range(4)] for i in range(num)]
    all = []
    # with open("soup_interest.txt",'w') as file:
    #     file.write(str(soup.prettify()))
    #     file.close()

    # print(soup.prettify())
    #判断是否有>的，比如 vested interests 和 credit
    # phrase-title dphrase-title 可以找到具体的词组英文
    # phrase-body dphrase_b 或  pr phrase-block dphrase-block 可以中英文释义
    # 得到这个，与后面得到的对比去重，得到最终的结果
    phrase = []
    phrase_title = []
    phrase_translation = []
    phrase_chinese = []
    phrase_english = []
    phrase_titles_span = soup.find_all(class_='phrase-title dphrase-title')
    # phrase_spans = soup.find_all(class_='phrase-body dphrase_b')
    for phrase_title_span in phrase_titles_span:
        # print(phrase_span)
        # print(phrase_title)
        pattern = r'>(.*?)<'
        phrase_title_span = re.findall(pattern, str(phrase_title_span))
        phrase_title_span = ''.join(phrase_title_span)
        # print(phrase_title_span)
        phrase_title.append(phrase_title_span)

        phrase_spans = soup.find_all(class_='phrase-body dphrase_b')
        if phrase_spans != None:
            for phrase_span in phrase_spans:
                pass
                # print("!!!!!!!!!!!!!!!!!!")
                # print(phrase_span)
                chinese_spans = phrase_span.find_all(class_='trans dtrans dtrans-se break-cj')
                #[<span class="trans dtrans dtrans-se break-cj" lang="zh-Hans">是…的骄傲;是…的光荣</span>]
                for chinese_span in chinese_spans:
                    # print("QQQQ")
                    # print(chinese_spans)
                    # print(chinese_span.string)
                    if chinese_span.string not in phrase_chinese:
                        phrase_chinese.append(chinese_span.string)
            # print(phrase_chinese)
                english_spans = phrase_span.find_all(class_='def ddef_d db')
                # print(english_spans)
                for english_span in english_spans:
                    pattern = r'>(.*?)<'
                    english_span = re.findall(pattern, str(english_span))
                    english_span = ''.join(english_span)
                    if english_span not in phrase_english:
                        phrase_english.append(english_span)
                    # all[i].append(english)
    # print(phrase_english)
    # print(phrase_chinese)
    # 获得phrase的translation
    if len(phrase_english) == len(phrase_chinese):
        for i in range(len(phrase_english)):
            one_phrase_translation = []
            one_phrase_translation.append(phrase_title[i])
            one_phrase_translation.append(phrase_english[i])
            one_phrase_translation.append(phrase_chinese[i])
            phrase_translation.append(one_phrase_translation)
    else:
        print("中英文释义不对应，debug！")
    # phrase_translation.pop(0)
    # print(phrase_translation)
    # print(len(phrase_translation))

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
    translation = []
    if len(chinese) == len(english):
        for i in range(len(chinese)):
            one_translation = []
            one_translation.append(word)
            one_translation.append(english[i])
            one_translation.append(chinese[i])
            translation.append(one_translation)
    else:
        print("chinese_num != english_num，中英文释义不对应，debug！")
    all_translation_en = [row[1] for row in translation]
    # print(all_translation_en)
    for one_phrase_translation in phrase_translation:
        if one_phrase_translation[1] in all_translation_en:
            i = all_translation_en.index(one_phrase_translation[1])
            translation.pop(i)
            all_translation_en.pop(i)

    print(translation)
    print(phrase_translation)
    # 最终结果是translation 和 phrase translation，如果没有phrase，后者就是空的
    return translation, phrase_translation
        # print(phrase_translation)
    # print("--------")

    # print(translation)
    # print(chinese_spans.span.string)
    # chinese_texts = re.findall(r'[\u4e00-\u9fff]+', soup.string)
    # print(soup.ul.get_text())
    # print([x.strip() for x in soup.ul.get_text().split('\n') if x.strip()])
def extract_web_new(url, headers, word,flag,num = 10,sentences = ""):
    #需要的元素有：英文、音标、英文中文释义，例句
    source_code = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source_code, 'html.parser')
    # all = [[j for j in range(4)] for i in range(num)]
    all = []
    # with open("soup_interest.txt",'w') as file:
    #     file.write(str(soup.prettify()))
    #     file.close()

    # print(soup.prettify())
    #判断是否有>的，比如 vested interests 和 credit
    # phrase-title dphrase-title 可以找到具体的词组英文
    # phrase-body dphrase_b 或  pr phrase-block dphrase-block 可以中英文释义
    # 得到这个，与后面得到的对比去重，得到最终的结果
    phrase = []
    phrase_title = []
    phrase_translation = []
    phrase_chinese = []
    phrase_english = []
    # pr phrase-block dphrase-block
    phrase_all_span = soup.find_all(class_=['pr phrase-block dphrase-block','pr phrase-block dphrase-block lmb-25'])
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
            # ['', 'and so on', '']
            for i in phrase_titles_span:
                if word in i:
                    current_phase.append(i)
                    break
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
            #[<span class="trans dtrans dtrans-se break-cj" lang="zh-Hans">是…的骄傲;是…的光荣</span>]
            for chinese_span in chinese_spans:
                if chinese_span.string not in phrase_chinese:
                    chi.append(chinese_span.string)
                    phrase_chinese.append(chinese_span.string)
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
            #['and all', ['and everything else', 'too'], ['以及其他一切；等等', '也']]
            phrase.append(current_phase)
    print(phrase)

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
        chinese.append(chinese_span)
    # 爬虫全部英文释义
    # english_spans = soup.find_all(class_='def ddef_d db')
    english_spans = soup.find_all(class_='def ddef_d db')
    english = []
    for english_span in english_spans:
        pattern = r'>(.*?)<'
        english_span = re.findall(pattern, str(english_span))
        english_span = ''.join(english_span)
        english.append(english_span)
        # all[i].append(english)
    translation = []
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
        print("chinese_num != english_num，中英文释义不对应，debug！")
    # all_translation_en = [row[1] for row in translation]
    # print(all_translation_en)
    for one_phrase_english in phrase_english:
        if one_phrase_english in english:
            i = english.index(one_phrase_english)
            translation[1].pop(i)
            translation[2].pop(i)

    print(translation)
    print(phrase)
    # 最终结果是translation 和 phrase translation，如果没有phrase，后者就是空的
    return translation, phrase
        # print(phrase_translation)
    # print("--------")

def get_cambridge_origin_pronoun_voice(soup, flag = 1):
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
        return None,None
    # print(origin[0])



    # 音标获取
    # <span class="ipa dipa lpr-2 lpl-1">ˈnaɪ.sə.ti</span>
    pronoun_spans = soup.find_all(class_='ipa dipa lpr-2 lpl-1')
    # print(pronoun_spans)
    # for pronoun_span in pronoun_spans:
    pronoun_pattern = r'>(.*?)<'
    pronoun_gets = re.findall(pronoun_pattern, str(pronoun_spans))
    for pronoun_get in pronoun_gets:
        if '/' in pronoun_get or pronoun_get[len(pronoun_get)-1] == '/' or len(pronoun_get) == 0:
            continue
        pronounciation = '/' + pronoun_get + '/'
        break
    # print(pronounciation)

    # voice网址获取
    voice_spans = soup.find_all('source',type='audio/mpeg')
    # print("voice_up_spans",voice_up_spans)
    pattern = re.compile(r'src="([^"]+\.mp3)"')

    for voice_span in voice_spans:
        match = pattern.search(str(voice_span))
        if match:
            extracted_voice = match.group(1)
            if "us_pron" in extracted_voice:
                url_voice = "https://dictionary.cambridge.org" + extracted_voice
                break
                pass
    print(url_voice)
    return origin[0], pronounciation
    pass

    # print(translation)
    # print(chinese_spans.span.string)
    # chinese_texts = re.findall(r'[\u4e00-\u9fff]+', soup.string)
    # print(soup.ul.get_text())
    # print([x.strip() for x in soup.ul.get_text().split('\n') if x.strip()])
if __name__ == '__main__':
    # guide url
    soup = read_web(guidURL + 'vlogger', headers)
    url = guidURL + 'vlogger'
    extract_web_new(url, headers,'vlogger ', 1)
    # get_cambridge_origin_pronoun_voice(soup)
    # extrac_web(guidURL + 'vested interest', 1)
    # for i in 'abcdefghijklmnopqrstuvwxyz':
    #     start(guidURL+i,1)

    # # extend url
    # for g in guideURLs:
    #     start(g, 2)
    # # 文件操作部分
    # fd = open('guideURLs.txt', 'w')  # 该文件保存26个首字母的url
    # print(guideURLs, file=fd)
    # fd.close()
    # fd = open('extendURLs.txt', 'w')  # 该文件保存所有单词的url
    # print(extendURLs, file=fd)
    # fd.close()

