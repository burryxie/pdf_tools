# -*- coding: utf-8 -*-
import os 
import sys
from PyQt5.QtWidgets import QApplication,QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



class PageNumberAdderGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.resize(300, 300)
        self.file_path_label = QLabel('PDF 文件路径:')
        self.file_path_line_edit = QLineEdit()
        self.browse_button = QPushButton('浏览')
        self.start_page_label = QLabel('起始页码:')
        self.start_page_line_edit = QLineEdit()
        self.start_page_line_edit.setText('1')
        self.alignment_label = QLabel('对齐方式:')
        self.alignment_combo_box = QComboBox()
        self.alignment_combo_box.addItems(['居中', '靠左', '靠右'])
        self.page_number_format_label = QLabel('页码格式:')
        self.page_number_format_combo_box = QComboBox()
        self.page_number_format_combo_box.addItems(['No.', '第No.页', '--No.--'])
        self.text_font_label = QLabel('字体格式:')
        self.text_font_label_combo_box = QComboBox()
        self.text_font_label_combo_box.addItems(['宋体', '仿宋体', '黑体', '楷体', '隶书'])
        self.add_page_numbers_button = QPushButton('添加页码')

        # 创建 QLabel 用于显示背景图片
        self.background_label = QLabel(self)

        # 设置背景图片

        layout = QVBoxLayout()
        # layout.addWidget(self.background_label)
        layout.addWidget(self.file_path_label)
        layout.addWidget(self.file_path_line_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.start_page_label)
        layout.addWidget(self.start_page_line_edit)
        layout.addWidget(self.alignment_label)
        layout.addWidget(self.alignment_combo_box)
        layout.addWidget(self.page_number_format_label)
        layout.addWidget(self.page_number_format_combo_box)
        layout.addWidget(self.text_font_label)
        layout.addWidget(self.text_font_label_combo_box)
        layout.addWidget(self.add_page_numbers_button)

        self.setLayout(layout)

        self.browse_button.clicked.connect(self.browse_pdf)
        self.add_page_numbers_button.clicked.connect(self.add_page_numbers)

        self.setWindowTitle('东宸数智\u2122 PDF文件添加页码工具')
        self.show()

    def browse_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('PDF 文件 (*.pdf)')
        file_path, _ = file_dialog.getOpenFileName()
        self.file_path_line_edit.setText(file_path)

    def add_page_numbers(self):
        file_path = self.file_path_line_edit.text()
        # start_page = int(self.start_page_line_edit.text())
        alignment_mapping = {'居中': 'center', '靠左': 'left', '靠右': 'right'}
        alignment = alignment_mapping[self.alignment_combo_box.currentText()]
        
        page_number_format_mapping = {'No.':'{page_number}' , '第No.页':'第{page_number}页' , '--No.--':'--{page_number}--' }
        page_number_format = page_number_format_mapping[self.page_number_format_combo_box.currentText()]
        
        font_mapping = {'宋体':'SongTi', '仿宋体':'FangSongTi', '黑体':'HeiTi', '楷体':'KaiTi', '隶书':'LishuTi'}
        font = font_mapping[self.text_font_label_combo_box.currentText()]
        
        if not os.path.exists(file_path):
            self.show_message_dialog("错误：文件不存在！请重新选择")
            return
                # 检查 start_page 是否为正整数
        try:
            start_page = int(self.start_page_line_edit.text())
            if start_page < 0:
                raise ValueError("起始页码必须是正整数")
        except ValueError:
            self.show_message_dialog("错误：起始页码必须是正整数")
            return
        
        page_number_adder = PageNumberAdder(file_path, start_page=start_page, alignment=alignment, page_number_format=page_number_format, font=font)
        result_pdf_bytes = page_number_adder.add_page_numbers_to_pdf()

        # 构建新的文件名
        base_file_name = QFileInfo(file_path).baseName()
        alignment_text = self.alignment_combo_box.currentText()
        save_file_name = f"{base_file_name}_添加页码_{alignment_text}.pdf"

        # 调用文件保存对话框
        save_dialog = QFileDialog()
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        save_dialog.setNameFilter('PDF 文件 (*.pdf)')
        save_dialog.setDefaultSuffix('pdf')
        # save_file_path, _ = save_dialog.getSaveFileName(dir=save_file_name)
        save_file_path, _ = save_dialog.getSaveFileName(None, '保存文件', save_file_name, 'PDF 文件 (*.pdf)', options=QFileDialog.Options())

        if save_file_path:
            with open(save_file_path, 'wb') as output_file:
                output_file.write(result_pdf_bytes)

            self.show_message_dialog(f"已添加页码，结果保存至: {save_file_path}")

    def show_message_dialog(self, message):
        msg_dialog = QMessageBox()
        msg_dialog.setText(message)
        msg_dialog.exec_()




class PageNumberAdder:
    # ...
    def __init__(self, file_path, start_page=1, alignment='center', page_number_format = '{page_number}', font = 'SongTi'):
        self.file_path = file_path
        self.start_page = start_page
        self.alignment = alignment
        self.page_number_format = page_number_format
        self.font = font
    
    def draw_rotated_text(self, can, x, y, text, angle):
        can.saveState()
        can.translate(x, y)
        can.rotate(angle)
        can.drawCentredString(0, 0, text)
        can.restoreState()

    def add_page_numbers_to_pdf(self):
        with open(self.file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()

            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                # page_number_text = page_number + self.start_page
                page_number_text = self.page_number_format.format(page_number=page_number + self.start_page)

                # 获取当前页面的大小。
                width, height = page.mediabox.upper_right
                width, height = float(width) / 2.83465, float(height) / 2.83465
                print(page_number, width, height, 'is_portrait' if height > width else 'not_portrait')

                # is_portrait
                if height > width :
                    # 如果当前页面的大小超过了 A4 的大小，则将其重新缩放至 A4 的大小。
                    if abs(width - 210) > 10 or abs(height - 297) > 10:
                        # 计算缩放比例。
                        scale_x = float(210 / width )
                        scale_y = float(297 / height)

                        # 将当前页面缩放至 A4 的大小。
                        page.scale(scale_x, scale_y)
                # not_portrait
                else:
                    if abs(width - 297) > 10 or abs(height - 210) > 10:
                        scale_x = float(297 / width )
                        scale_y = float(210 / height)

                        # 将当前页面缩放至 A4 的大小。
                        page.scale(scale_x, scale_y)



                packet = io.BytesIO()
                can = canvas.Canvas(packet)

                # 获取页面的旋转方向
                rotation = page.get('/Rotate', 0)
                print(page_number, rotation)
                rotation_to_zero = (360 - rotation) % 360
                if rotation_to_zero:
                    page.rotate(rotation_to_zero)
                    # print(page_number, page.get('/Rotate', 0))
                    page.rotate(rotation)
                # page['/Rotate'] = rotation
                # short_side = min(page.mediabox.width, page.mediabox.height)

                if rotation == 270:
                    x_coordinate = 20  # 默认纵坐标 
                    if self.alignment == 'left':
                        y_coordinate = float(page.mediabox.height) - 20.0
                    elif self.alignment == 'center':
                        y_coordinate = float(page.mediabox.height) / 2.0
                    elif self.alignment == 'right':
                        y_coordinate = 20
                    else:
                        raise ValueError("Invalid alignment. Use 'left', 'center', or 'right'.")
                    
                elif rotation == 90:
                    x_coordinate = float(page.mediabox.width) - 20.0  # 默认纵坐标 
                    if self.alignment == 'left':
                        y_coordinate = 20.0
                    elif self.alignment == 'center':
                        y_coordinate = float(page.mediabox.height) / 2.0
                    elif self.alignment == 'right':
                        y_coordinate = float(page.mediabox.height) - 20.0
                    else:
                        raise ValueError("Invalid alignment. Use 'left', 'center', or 'right'.")
                elif rotation == 180:
                    y_coordinate = float(page.mediabox.height) - 20.0  # 默认纵坐标 
                    if self.alignment == 'left':
                        x_coordinate = float(page.mediabox.width) - 20.0
                    elif self.alignment == 'center':
                        x_coordinate = float(page.mediabox.width) / 2.0
                    elif self.alignment == 'right':
                        x_coordinate = 20.0
                    else:
                        raise ValueError("Invalid alignment. Use 'left', 'center', or 'right'.")
                else:
                    if self.alignment == 'left':
                        x_coordinate = 20
                    elif self.alignment == 'center':
                        x_coordinate = float(page.mediabox.width) / 2.0
                    elif self.alignment == 'right':
                        x_coordinate = float(page.mediabox.width) - 20.0
                    else:
                        raise ValueError("Invalid alignment. Use 'left', 'center', or 'right'.")

                    y_coordinate = 20  # 默认纵坐标
                

                can.setFont(self.font, 12)
                # can.setFont("Helvetica", 12)
                self.draw_rotated_text(can, x_coordinate, y_coordinate, page_number_text, rotation)
                can.save()

                packet.seek(0)
                new_pdf = PdfReader(packet)
                new_page = new_pdf.pages[0]

                page.merge_page(new_page)
                pdf_writer.add_page(page)

            result_pdf_bytes = io.BytesIO()
            pdf_writer.write(result_pdf_bytes)
            return result_pdf_bytes.getvalue()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 主函数
if __name__ == '__main__':
    # 注册自定义字体
    pdfmetrics.registerFont(TTFont('SongTi', resource_path('fonts/chinese/STSong.ttf')))
    pdfmetrics.registerFont(TTFont('FangSongTi', resource_path('fonts/chinese/STFangsong.ttf')))
    pdfmetrics.registerFont(TTFont('HeiTi', resource_path('fonts/chinese/STHeiti.ttf')))
    pdfmetrics.registerFont(TTFont('KaiTi', resource_path('fonts/chinese/STKaiti.ttf')))
    pdfmetrics.registerFont(TTFont('LishuTi', resource_path('fonts/chinese/STLiti.ttf')))

    app = QApplication(sys.argv)
    ex = PageNumberAdderGUI()
    sys.exit(app.exec_())
