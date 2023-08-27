from Economist_anki import Economists
from notion_patch_all_anki import Update_anki


if __name__ == "__main__":
    print("这是一个基于notion、python、anki、文章的背单词项目\n"
          "在运行前请确认一下几件事：\n"
          "1. 根据readme.md，获得notion的api接口、必要的python包等\n"
          "2. 关闭vpn(上传notion可能与vpn冲突)\n"
          "3. 根据readme了解基本流程")
    while True:
        selection = input("输入本次要做的事情：\n"
                          "1. 读新文章\n"
                          "2. 更新database\n"
                          "3. 退出流程\n")
        if selection == "3":
            break
        elif selection == "2":
            a = Update_anki()
            a.patch_update()
        elif selection == "1":
            a = Economists()
            a.run()
    print("本次运行结束")