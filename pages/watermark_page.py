from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                           QLineEdit, QGridLayout, QFrame, QFileDialog, QMessageBox, QSpinBox)
from PyQt6.QtCore import Qt
from styles.style import get_page_style
from .base_page import BasePage
from tools.pdf_watermark import pdf_watermark
import os

class WatermarkPage(BasePage):
    def __init__(self):
        super().__init__("PDF 加水印")
        
        # 设置样式
        self.setStyleSheet(get_page_style())
        
        # 文件选择区域
        file_frame = QFrame()
        file_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        file_layout = QGridLayout(file_frame)
        
        # 输入文件选择
        self.input_label = QLabel("选择PDF文件:")
        self.input_edit = QLineEdit()
        self.input_edit.setReadOnly(True)
        self.input_button = QPushButton("浏览...")
        self.input_button.clicked.connect(self.select_input_file)
        
        file_layout.addWidget(self.input_label, 0, 0)
        file_layout.addWidget(self.input_edit, 0, 1)
        file_layout.addWidget(self.input_button, 0, 2)
        
        # 输出文件选择
        self.output_label = QLabel("输出文件:")
        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)
        self.output_button = QPushButton("浏览...")
        self.output_button.clicked.connect(self.select_output_file)
        
        file_layout.addWidget(self.output_label, 1, 0)
        file_layout.addWidget(self.output_edit, 1, 1)
        file_layout.addWidget(self.output_button, 1, 2)
        
        self.layout.addWidget(file_frame)
        
        # 水印设置区域
        watermark_frame = QFrame()
        watermark_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        watermark_layout = QGridLayout(watermark_frame)
        
        # 水印文本输入
        self.text_label = QLabel("水印文本:")
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("请输入要添加的水印文字...")
        
        watermark_layout.addWidget(self.text_label, 0, 0)
        watermark_layout.addWidget(self.text_edit, 0, 1)
        
        # 水印设置
        self.font_label = QLabel("字体大小:")
        self.font_size = QSpinBox()
        self.font_size.setRange(10, 72)
        self.font_size.setValue(36)
        
        watermark_layout.addWidget(self.font_label, 1, 0)
        watermark_layout.addWidget(self.font_size, 1, 1)
        
        self.opacity_label = QLabel("不透明度:")
        self.opacity = QSpinBox()
        self.opacity.setRange(1, 100)
        self.opacity.setValue(30)
        
        watermark_layout.addWidget(self.opacity_label, 2, 0)
        watermark_layout.addWidget(self.opacity, 2, 1)
        
        self.layout.addWidget(watermark_frame)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.watermark_button = QPushButton("添加水印")
        self.watermark_button.clicked.connect(self.add_watermark)
        button_layout.addWidget(self.watermark_button)
        
        self.layout.addLayout(button_layout)
        
        # 添加进度条和状态标签
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.status_label)
        
        # 添加底部空白
        self.layout.addStretch()
        
    def select_input_file(self):
        """选择输入文件"""
        file_name = self.select_file("选择要添加水印的PDF文件")
        if file_name:
            self.input_edit.setText(file_name)
            # 自动设置输出文件名
            dir_name = os.path.dirname(file_name)
            base_name = os.path.splitext(os.path.basename(file_name))[0]
            output_file = os.path.join(dir_name, f"{base_name}_watermark.pdf")
            self.output_edit.setText(output_file)
            
    def select_output_file(self):
        """选择输出文件"""
        file_name = self.save_file("保存添加水印后的PDF文件")
        if file_name:
            self.output_edit.setText(file_name)
            
    def add_watermark(self):
        """添加水印"""
        input_file = self.input_edit.text()
        output_file = self.output_edit.text()
        watermark_text = self.text_edit.text()
        font_size = self.font_size.value()
        opacity = self.opacity.value() / 100.0
        
        if not input_file:
            QMessageBox.warning(self, "警告", "请选择要添加水印的PDF文件")
            return
            
        if not output_file:
            QMessageBox.warning(self, "警告", "请选择输出文件位置")
            return
            
        if not watermark_text:
            QMessageBox.warning(self, "警告", "请输入水印文本")
            return
            
        try:
            from tools.pdf_watermark import pdf_watermark
            
            # 显示进度条
            self.progress.setMaximum(100)
            self.progress.setValue(0)
            self.progress.show()
            
            # 调用水印函数
            pdf_watermark(input_file, output_file, watermark_text, font_size, opacity)
            
            self.progress.setValue(100)
            self.show_message("PDF水印添加完成！")
            
            # 打开输出文件所在目录
            import platform
            output_dir = os.path.dirname(output_file)
            if platform.system() == 'Windows':
                os.startfile(output_dir)
            elif platform.system() == 'Darwin':  # macOS
                os.system(f'open "{output_dir}"')
            else:  # Linux
                os.system(f'xdg-open "{output_dir}"')
            
        except Exception as e:
            self.show_message(f"发生错误: {str(e)}", True)
            QMessageBox.critical(self, "错误", str(e))
            
        finally:
            self.progress.hide() 