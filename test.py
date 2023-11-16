import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("背景图片示例")
        self.setGeometry(100, 100, 800, 600)

        # 创建 QLabel 用于显示背景图片
        self.background_label = QLabel(self)

        # 设置背景图片
        self.set_background_image("./images/chiang-mai.jpg")

        # 创建布局，并将 QLabel 添加到布局中
        layout = QVBoxLayout(self)
        layout.addWidget(self.background_label)

    def set_background_image(self, image_path):
        # 通过 QPixmap 加载图片
        pixmap = QPixmap(image_path)

        # 设置 QLabel 的大小为窗口大小，并设置背景图片
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setPixmap(pixmap.scaled(self.width(), self.height()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
