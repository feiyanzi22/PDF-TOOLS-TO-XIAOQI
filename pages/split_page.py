from .base_page import BasePage
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QSpinBox, QRadioButton, QButtonGroup, QFileDialog,
                            QMessageBox, QLineEdit, QGridLayout, QFrame)
from PyQt6.QtCore import Qt
import os
from styles.style import get_page_style  # 添加导入

class SplitPage(BasePage):
    def __init__(self):
        super().__init__("PDF 拆分")
        
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
        
        # 拆分方式选择
        split_frame = QFrame()
        split_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        split_layout = QVBoxLayout(split_frame)
        
        split_label = QLabel("拆分方式:")
        split_layout.addWidget(split_label)
        
        self.split_group = QButtonGroup()
        
        # 按页数拆分
        self.by_pages = QRadioButton("按固定页数拆分")
        self.by_pages.setChecked(True)
        self.pages_spin = QSpinBox()
        self.pages_spin.setRange(1, 9999)
        self.pages_spin.setValue(1)
        
        pages_layout = QHBoxLayout()
        pages_layout.addWidget(self.by_pages)
        pages_layout.addWidget(self.pages_spin)
        pages_layout.addWidget(QLabel("页/个文件"))
        pages_layout.addStretch()
        
        split_layout.addLayout(pages_layout)
        self.split_group.addButton(self.by_pages, 0)
        
        # 按文件数拆分
        self.by_files = QRadioButton("平均拆分为")
        self.files_spin = QSpinBox()
        self.files_spin.setRange(2, 100)
        self.files_spin.setValue(2)
        
        files_layout = QHBoxLayout()
        files_layout.addWidget(self.by_files)
        files_layout.addWidget(self.files_spin)
        files_layout.addWidget(QLabel("个文件"))
        files_layout.addStretch()
        
        split_layout.addLayout(files_layout)
        self.split_group.addButton(self.by_files, 1)
        
        self.layout.addWidget(split_frame)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.split_button = QPushButton("开始拆分")
        self.split_button.clicked.connect(self.split_pdf)
        button_layout.addWidget(self.split_button)
        
        self.layout.addLayout(button_layout)
        
        # 添加进度条和状态标签
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.status_label)
        
        # 添加底部空白
        self.layout.addStretch()
        
    def select_input_file(self):
        """选择输入文件"""
        file_name = self.select_file("选择要拆分的PDF文件")
        if file_name:
            self.input_edit.setText(file_name)
            # 创建与输入文件同名的输出目录
            pdf_dir = os.path.dirname(file_name)
            pdf_name = os.path.splitext(os.path.basename(file_name))[0]
            output_dir = os.path.join(pdf_dir, pdf_name)
            self.output_edit.setText(output_dir)
            
    def select_output_dir(self):
        """选择输出目录"""
        folder = self.select_folder("选择输出目录")
        if folder:
            self.output_edit.setText(folder)
            
    def split_pdf(self):
        """拆分PDF文件"""
        input_file = self.input_edit.text()
        output_dir = self.output_edit.text()
        
        if not input_file:
            QMessageBox.warning(self, "警告", "请选择要拆分的PDF文件")
            return
            
        try:
            # 确保输出目录存在
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            from tools.pdf_split import pdf_split
            
            # 显示进度条
            self.progress.setMaximum(100)
            self.progress.setValue(0)
            self.progress.show()
            
            # 获取拆分参数
            if self.split_group.checkedId() == 0:  # 按页数拆分
                pages_per_file = self.pages_spin.value()
                pdf_split(input_file, output_dir, pages_per_file=pages_per_file)
            else:  # 按文件数拆分
                num_files = self.files_spin.value()
                pdf_split(input_file, output_dir, num_files=num_files)
            
            self.progress.setValue(100)
            self.show_message(f"PDF拆分完成！文件保存在：{output_dir}")
            
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