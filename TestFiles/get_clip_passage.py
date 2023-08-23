import pyperclip
import time
import subprocess
import chardet
def get_clip_passage():
    pyperclip.copy('')
    # 初始上一次的剪切板内容为空
    prev_clipboard_content = ''
    with open("passage.txt", 'w', encoding='utf-8') as file:
        file.truncate()
    print("检查clash是否关闭")
    input("文档已经清空，enter开始运行")
    while True:
        # 获取剪切板内容
        time.sleep(5)
        clipboard_content = pyperclip.paste()
        clipboard_content = clipboard_content.strip()

        # # 如果剪切板内容发生变化且不为空，则写入到txt文件中
        # if clipboard_content != prev_clipboard_content and clipboard_content and clipboard_content not in self.words:
        with open("passage.txt", 'w', encoding='utf-8') as file:
            file.write(clipboard_content)
        print(clipboard_content)
                # self.words.append(clipboard_content)
            # 更新上一次的剪切板内容为当前内容
            # prev_clipboard_content = clipboard_content
        resp = input("文章全部复制了？ 1/0")
        if resp == "1":
            break
        # 每隔一秒钟检查一次剪切板内容
        time.sleep(1)
    subprocess.run(['notepad.exe', "passage.txt"], check=True)

if __name__ == "__main__":
    get_clip_passage()