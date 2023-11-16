import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import QProcess
import subprocess
from pdf_add_page_number import PageNumberAdderGUI


class EntryWindow(QPushButton):
    def __init__(self):
        super(EntryWindow, self).__init__()

        self.setWindowTitle('东宸数智\u2122   PDF工具箱')
        self.resize(300, 100)
        # 创建按钮
        self.pdf_add_page_number_button = QPushButton("添加页码")
        self.pdf_add_page_number_button.clicked.connect(self.pdf_add_page_number_button)

        # 创建垂直布局管理器
        layout = QVBoxLayout(self)

        # 将按钮添加到布局中
        layout.addWidget(self.pdf_add_page_number_button)

    def pdf_add_page_number_button(self):
        # 在按钮点击时打开另一个程序
        # program_path = "pdf_add_page_number.py"  # 替换为你的程序路径
        # # QProcess.startDetached(sys.executable, [sys.executable, program_path])
        # process = QProcess()
        # process.start("python", [program_path])

        # app_a = QApplication([])  # 创建一个新的应用程序实例
        # program_a = PageNumberAdderGUI()  # 创建 ProgramA 窗口
        # program_a.show()
        # sys.exit(app_a.exec_())
        
        program_a_path = "pdf_add_page_number.py"  # 替换为你的程序路径
        # subprocess.Popen(["python", program_a_path])
        process = QProcess()
        process.start("python", [program_a_path])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    entry_window = EntryWindow()
    entry_window.show()

    sys.exit(app.exec_())
