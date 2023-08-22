# import pyautogui
#
# import win32clipboard
# import win32con
# import cv2
#
# # pyautogui.click(x=413, y=207, clicks=2, interval=0.25)
# # pyautogui.hotkey('ctrl', 'c')
# # win32clipboard.OpenClipboard()
# # code = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
# # win32clipboard.CloseClipboard()
#
# # pyautogui.click(x=800, y=800, clicks=1, interval=0.25)
# # im1 = pyautogui.screenshot()
# im2 = pyautogui.screenshot('my_screenshot.png')
#
# # 执行鼠标滚轮的滚动。垂直滚动还是水平滚动取决于底层操作系统。
# import pywinauto.mouse
# # pywinauto.mouse.scroll((1100,300),1000) #(1100,300)是初始坐标，1000是滑动距离（可负）
# # pyautogui.scroll(-50)  # scroll down 50 "clicks"
# notion_path = "my_screenshot.png"
# notion = cv2.imread(notion_path)
# # cv2.imshow("1",notion)
# # cv2.waitKey(0)
# notion_position = pyautogui.locateOnScreen('notion.png', grayscale=True, confidence= 0.7)
#
# notion_center = pyautogui.center(notion_position)
# pyautogui.click(notion_center, clicks=1, interval=0.25)
#
# import  os
# import  time
# import pyautogui as pag
# try:
#     while True:
#         print("Press Ctrl-C to end")
#         screenWidth, screenHeight = pag.size()  #获取屏幕的尺寸
#         print(screenWidth,screenHeight)
#         x,y = pag.position()   #获取当前鼠标的位置
#         posStr = "Position:" + str(x).rjust(4)+','+str(y).rjust(4)
#         print(posStr)
#         time.sleep(0.2)
#         os.system('cls')   #清楚屏幕
# except KeyboardInterrupt:
#     print('end....')