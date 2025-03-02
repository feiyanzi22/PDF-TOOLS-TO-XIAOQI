from tkinter import messagebox
from .base_page import BasePage
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QLineEdit, QGridLayout, QFrame)
from PyQt6.QtCore import Qt
from styles.style import get_page_style
import os

class DecryptPage(BasePage):
    def __init__(self):
        super().__init__("PDF 解密")
        
        # 设置样式
        self.setStyleSheet(get_page_style())
        
        # 文件选择区域
        file_frame = QFrame()
        file_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        file_layout = QGridLayout(file_frame)
        
        # 输入文件选择
        self.input_label = QLabel("选择加密的PDF文件:")
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
        
        # 密码输入区域
        password_frame = QFrame()
        password_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        password_layout = QGridLayout(password_frame)
        
        # 密码输入
        self.pwd_label = QLabel("输入密码:")
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        
        password_layout.addWidget(self.pwd_label, 0, 0)
        password_layout.addWidget(self.pwd_edit, 0, 1)
        
        self.layout.addWidget(password_frame)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.decrypt_button = QPushButton("解密PDF")
        self.decrypt_button.clicked.connect(self.decrypt_pdf)
        button_layout.addWidget(self.decrypt_button)
        
        self.layout.addLayout(button_layout)
        
        # 添加进度条和状态标签
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.status_label)
        
        # 添加底部空白
        self.layout.addStretch()
        
    def select_input_file(self):
        """选择输入文件"""
        file_name = self.select_file("选择要解密的PDF文件")
        if file_name:
            self.input_edit.setText(file_name)
            # 自动设置输出文件名
            dir_name = os.path.dirname(file_name)
            base_name = os.path.splitext(os.path.basename(file_name))[0]
            output_file = os.path.join(dir_name, f"{base_name}_decrypted.pdf")
            self.output_edit.setText(output_file)
            
    def select_output_file(self):
        """选择输出文件"""
        file_name = self.save_file("保存解密后的PDF文件")
        if file_name:
            self.output_edit.setText(file_name)
            
    def decrypt_pdf(self):
        """解密PDF文件"""
        input_file = self.input_edit.text()
        output_file = self.output_edit.text()
        password = self.pwd_edit.text()
        
        if not input_file:
            messagebox.warning(self, "警告", "请选择要解密的PDF文件")
            return
            
        if not output_file:
            messagebox.warning(self, "警告", "请选择输出文件位置")
            return
            
        if not password:
            messagebox.warning(self, "警告", "请输入密码")
            return
            
        try:
            from tools.pdf_decrypt import pdf_decrypt
            
            # 显示进度条
            self.progress.setMaximum(100)
            self.progress.setValue(0)
            self.progress.show()
            
            # 调用解密函数
            pdf_decrypt(input_file, output_file, password)
            
            self.progress.setValue(100)
            self.show_message("PDF解密完成！")
            
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
            messagebox.critical(self, "错误", str(e))
            
        finally:
            self.progress.hide() 