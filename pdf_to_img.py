# -*- coding: utf-8 -*-
import os 
import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QSizePolicy, QSpacerItem, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIntValidator
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import fitz  # PyMuPDF



class PdfToImageGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.resize(300, 300)
        self.input_file_path_label = QLabel('PDF 文件路径:')
        self.input_file_path_line_edit = QLineEdit()
        self.input_browse_button = QPushButton('浏览')
        self.output_file_path_label = QLabel('图片保存路径:')
        self.output_file_path_line_edit = QLineEdit()
        self.output_browse_button = QPushButton('浏览')
        self.image_format_label = QLabel('输出文件格式:')
        self.image_format_combo_box = QComboBox()
        self.image_format_combo_box.addItems(['JPEG', 'BMP', 'PNG', 'TIFF'])
        self.pdf_to_images_button = QPushButton('开始转换')

        # 创建 QLabel 用于显示背景图片
        self.background_label = QLabel(self)

        # 创建水平布局
        hbox = QHBoxLayout()

        # 将标签和输入框添加到水平布局中
        self.start_page_label = QLabel('起始页数:')
        self.start_page_value = QLineEdit(self)
        self.start_page_value.setText("1")  # 设置占位文本
        self.end_page_label = QLabel('结束页数:')
        self.end_page_value = QLineEdit(self)
        hbox.addWidget(self.start_page_label)
        hbox.addWidget(self.start_page_value)
        hbox.addWidget(self.end_page_label)
        hbox.addWidget(self.end_page_value)
        int_validator = QIntValidator()
        self.start_page_value.setValidator(int_validator)
        self.end_page_value.setValidator(int_validator)

        layout = QVBoxLayout()
        # layout.addWidget(self.background_label)
        layout.addWidget(self.input_file_path_label)
        layout.addWidget(self.input_file_path_line_edit)
        layout.addWidget(self.input_browse_button)
        layout.addLayout(hbox)
        spacer = QSpacerItem(300, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        layout.addWidget(self.image_format_label)
        layout.addWidget(self.image_format_combo_box)
        layout.addWidget(self.output_file_path_label)
        layout.addWidget(self.output_file_path_line_edit)
        layout.addWidget(self.output_browse_button)
        layout.addWidget(self.pdf_to_images_button)

        self.setLayout(layout)

        self.input_browse_button.clicked.connect(self.input_browse_pdf)
        self.output_browse_button.clicked.connect(self.output_browse_pdf)
        self.pdf_to_images_button.clicked.connect(self.extract_and_save_images)

        self.setWindowTitle('东宸数智\u2122 PDF转图片工具')
        self.show()

    def input_browse_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('PDF 文件 (*.pdf)')
        file_path, _ = file_dialog.getOpenFileName()
        self.input_file_path_line_edit.setText(file_path)

    def output_browse_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹', options=options)

        if folder_path:
            print(f'选择的文件夹路径: {folder_path}')
            self.output_file_path_line_edit.setText(folder_path)


    def extract_and_save_images(self):
        if not os.path.exists(self.input_file_path_line_edit.text()):
            self.show_message_dialog("错误：pdf文件不存在！请重新选择")
            return
        
        if not os.path.exists(self.output_file_path_line_edit.text()):
            self.show_message_dialog("错误：输出文件夹不存在！请重新选择")
            return
        
        start_page = int(self.start_page_value.text())
        try:
            end_page = int(self.end_page_value.text())
        except:
            end_page = 100000
        if start_page <= 0:
            self.show_message_dialog("起始页码必须是正整数")
            return 
        elif start_page > end_page:
            self.show_message_dialog("请检查起始页码和结束页码设置")
            return 

        image_format_suffix_mapping = {'JPEG':'.jpg', 'BMP':'.bmp', 'PNG':'.png', 'TIFF':'.tiff'}
        image_format_suffix = image_format_suffix_mapping[self.image_format_combo_box.currentText()]


        doc = fitz.open(self.input_file_path_line_edit.text())
    
        for page_num in range(start_page - 1, min(doc.page_count, end_page)):
            page = doc[page_num]
            pix = page.get_pixmap()
            
            image_path = self.output_file_path_line_edit.text()+f"/image_{page_num + 1}"+image_format_suffix
            
            # 将 pixmap 转换为 PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(image_path, self.image_format_combo_box.currentText())
            
            print(f"Image saved: {image_path}")

        doc.close()
        self.show_message_dialog("转换完成图片已保存至"+self.output_file_path_line_edit.text())
        

    def show_message_dialog(self, message):
        msg_dialog = QMessageBox()
        msg_dialog.setText(message)
        msg_dialog.exec_()

# 主函数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PdfToImageGUI()
    sys.exit(app.exec_())
