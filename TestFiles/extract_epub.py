from bs4 import BeautifulSoup

def exact_p_tag(path):
    xhtml_file = open(path,'r', encoding='utf-8')
    xhtml_handle = xhtml_file.read()

    soup = BeautifulSoup(xhtml_handle,'lxml')

    title = soup.find_all("title")

    p_list = soup.find_all('p')
    for p in p_list:
        print(p.text)

import ebooklib
from ebooklib import epub

def ebooklib_exact(path):
   book = epub.read_epub(path)
   cover_image_data = None
   text_content = ""
   for item in book.items:
       if item.get_type() == ebooklib.ITEM_COVER:
           cover_image_data = item.get_content()
           break

   for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
       if len(item.get_content()) != 0:
           # print(item.get_content())
           text_content += str(item.get_content())

   return cover_image_data, text_content

import ebooklib
from ebooklib import epub

def extract_epub_content(epub_file):
    # 打开EPUB文件
    book = epub.read_epub(epub_file)

    # 用于存储提取的文本内容
    extracted_content = ""

    # 遍历书籍的每个章节
    for item in book.get_items():
        # 提取文本内容
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            extracted_content += item.get_content()

    return extracted_content




import zlib

if __name__ == "__main__":
    # epub_path = "D:/epub/TE-2023-05-13-EPUB.epub"
    epub_path =  "E:/TsinghuaCloud/Seafile/Economist/2023-3-11/TE-2023-03-11-EPUB.epub"
    print(extract_epub_content(epub_path))
    # exact_p_tag("D:/epub/TE-2023-05-13-EPUB.epub")
    # cover, text = ebooklib_exact(epub_path)
    # if cover:
    #     with open('cover.jpg', 'wb') as f:
    #         f.write(cover)
    #
    # # 打印文本内容
    # with open('epub.txt', 'w') as f:
    #     # compressed = zlib.compress(text.encode())
    #     f.write(text)
    # print(text)