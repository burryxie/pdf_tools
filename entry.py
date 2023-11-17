from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import QProcess
import sys

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(300, 300)
        self.initUI()


    def show_message_dialog(self, message):
        msg_dialog = QMessageBox()
        msg_dialog.setText(message)
        msg_dialog.exec_()

    def initUI(self):
        self.setWindowTitle('东宸数智\u2122  PDF工具箱')
        

        add_page_number = QPushButton('添加页码', self)
        add_page_number.clicked.connect(self.add_page_number)

        pdf_to_img = QPushButton('提取图片', self)
        pdf_to_img.clicked.connect(self.pdf_to_img)

        to_be_added = QPushButton('敬请期待', self)
        to_be_added.clicked.connect(self.to_be_added)

        vbox = QVBoxLayout()
        vbox.addWidget(add_page_number)
        vbox.addWidget(pdf_to_img)
        vbox.addWidget(to_be_added)

        self.setLayout(vbox)
        self.show()

        # 在这里创建 QProcess 对象
        self.process = QProcess(self)

    def add_page_number(self):
        # 设置要启动的程序
        self.process.start('python', ['pdf_add_page_number.py'])

    def pdf_to_img(self):
        # 设置要启动的程序
        self.process.start('python', ['pdf_to_img.py'])



    def to_be_added(self):
        self.show_message_dialog("更多功能，敬请期待")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
