from .base_page import BasePage
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QLineEdit, QGridLayout, QFrame, QMessageBox,
                            QSpinBox, QComboBox, QCheckBox)
from PyQt6.QtCore import Qt
from styles.style import get_page_style
import os

class ToImagePage(BasePage):
    def __init__(self):
        super().__init__("PDF 转图片")
        
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
        
        # 输出目录选择
        self.output_label = QLabel("输出目录:")
        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)
        self.output_button = QPushButton("浏览...")
        self.output_button.clicked.connect(self.select_output_dir)
        
        file_layout.addWidget(self.output_label, 1, 0)
        file_layout.addWidget(self.output_edit, 1, 1)
        file_layout.addWidget(self.output_button, 1, 2)
        
        self.layout.addWidget(file_frame)
        
        # 转换设置区域
        settings_frame = QFrame()
        settings_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        settings_layout = QGridLayout(settings_frame)
        
        # 图片格式选择
        self.format_label = QLabel("图片格式:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG", "BMP", "TIFF"])
        self.format_combo.setStyleSheet("QComboBox { color: #333333; }")  # 设置文字颜色
        
        settings_layout.addWidget(self.format_label, 0, 0)
        settings_layout.addWidget(self.format_combo, 0, 1)
        
        # DPI设置
        self.dpi_label = QLabel("图片DPI:")
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(72, 600)
        self.dpi_spin.setValue(300)
        self.dpi_spin.setSingleStep(72)
        
        settings_layout.addWidget(self.dpi_label, 1, 0)
        settings_layout.addWidget(self.dpi_spin, 1, 1)
        
        # 质量设置（仅用于JPEG）
        self.quality_label = QLabel("图片质量:")
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(95)
        
        settings_layout.addWidget(self.quality_label, 2, 0)
        settings_layout.addWidget(self.quality_spin, 2, 1)
        
        # 是否转换所有页面
        self.all_pages = QCheckBox("转换所有页面")
        self.all_pages.setChecked(True)
        settings_layout.addWidget(self.all_pages, 3, 0, 1, 2)
        
        self.layout.addWidget(settings_frame)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.convert_button = QPushButton("开始转换")
        self.convert_button.clicked.connect(self.convert_to_image)
        button_layout.addWidget(self.convert_button)
        
        self.layout.addLayout(button_layout)
        
        # 添加进度条和状态标签
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.status_label)
        
        # 添加底部空白
        self.layout.addStretch()
        
    def select_input_file(self):
        """选择输入文件"""
        file_name = self.select_file("选择要转换的PDF文件")
        if file_name:
            self.input_edit.setText(file_name)
            # 自动设置输出目录
            dir_name = os.path.dirname(file_name)
            base_name = os.path.splitext(os.path.basename(file_name))[0]
            output_dir = os.path.join(dir_name, f"{base_name}_images")
            self.output_edit.setText(output_dir)
            
    def select_output_dir(self):
        """选择输出目录"""
        folder = self.select_folder("选择输出目录")
        if folder:
            self.output_edit.setText(folder)
            
    def convert_to_image(self):
        """转换PDF为图片"""
        input_file = self.input_edit.text()
        output_dir = self.output_edit.text()
        
        if not input_file:
            QMessageBox.warning(self, "警告", "请选择要转换的PDF文件")
            return
            
        if not output_dir:
            QMessageBox.warning(self, "警告", "请选择输出目录")
            return
            
        try:
            from tools.pdf_to_image import pdf_to_image
            
            # 显示进度条
            self.progress.setMaximum(100)
            self.progress.setValue(0)
            self.progress.show()
            
            # 获取转换参数
            format = self.format_combo.currentText().lower()
            dpi = self.dpi_spin.value()
            all_pages = self.all_pages.isChecked()
            
            # 调用转换函数
            pdf_to_image(
                input_file=input_file,
                output_dir=output_dir,
                format=format,
                dpi=dpi,
                all_pages=all_pages
            )
            
            self.progress.setValue(100)
            self.show_message("PDF转换完成！")
            
            # 打开输出目录
            import platform
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