import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QComboBox, QLabel, QWidget
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建按钮
        self.button1 = QPushButton("1", self)
        self.button1.clicked.connect(self.button_clicked)

        self.button2 = QPushButton("2", self)
        self.button2.clicked.connect(self.button_clicked)

        self.button3 = QPushButton("3", self)
        self.button3.clicked.connect(self.button_clicked)

        # 设置主窗口布局
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 初始化标签
        self.label = QLabel("等待按钮输入", self)
        layout.addWidget(self.label)

    def button_clicked(self):
        sender = self.sender()
        if sender:
            button_text = sender.text()
            if button_text == "1":
                self.label.setText("您点击了按钮1，执行操作1")
                print("您点击了1")
            elif button_text == "2":
                self.label.setText("您点击了按钮2，执行操作2")
                print("您点击了2")
            elif button_text == "3":
                self.label.setText("您点击了按钮3，执行操作3")
                print("您点击了3")

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
