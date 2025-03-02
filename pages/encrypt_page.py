from .base_page import BasePage
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QLineEdit, QGridLayout, QFrame, QCheckBox,
                            QMessageBox)
from PyQt6.QtCore import Qt
from styles.style import get_page_style
import os

class EncryptPage(BasePage):
    def __init__(self):
        super().__init__("PDF 加密")
        
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
        
        # 密码设置区域
        password_frame = QFrame()
        password_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        password_layout = QGridLayout(password_frame)
        
        # 用户密码（打开密码）
        self.user_pwd_check = QCheckBox("设置打开密码")
        self.user_pwd_check.setChecked(True)
        self.user_pwd_edit = QLineEdit()
        self.user_pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.user_pwd_check.toggled.connect(self.user_pwd_edit.setEnabled)
        
        password_layout.addWidget(self.user_pwd_check, 0, 0)
        password_layout.addWidget(self.user_pwd_edit, 0, 1)
        
        # 所有者密码（权限密码）
        self.owner_pwd_check = QCheckBox("设置权限密码")
        self.owner_pwd_edit = QLineEdit()
        self.owner_pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.owner_pwd_edit.setEnabled(False)
        self.owner_pwd_check.toggled.connect(self.owner_pwd_edit.setEnabled)
        
        password_layout.addWidget(self.owner_pwd_check, 1, 0)
        password_layout.addWidget(self.owner_pwd_edit, 1, 1)
        
        self.layout.addWidget(password_frame)
        
        # 权限设置区域
        perm_frame = QFrame()
        perm_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        perm_layout = QVBoxLayout(perm_frame)
        
        perm_label = QLabel("PDF权限设置:")
        perm_layout.addWidget(perm_label)
        
        # 权限复选框
        self.print_check = QCheckBox("允许打印")
        self.modify_check = QCheckBox("允许修改")
        self.copy_check = QCheckBox("允许复制内容")
        self.annotate_check = QCheckBox("允许添加注释")
        
        # 默认全部允许
        for check in [self.print_check, self.modify_check, 
                     self.copy_check, self.annotate_check]:
            check.setChecked(True)
            check.setEnabled(False)
            perm_layout.addWidget(check)
        
        # 连接权限密码复选框的状态变化
        self.owner_pwd_check.toggled.connect(self.toggle_permissions)
        
        self.layout.addWidget(perm_frame)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.encrypt_button = QPushButton("加密PDF")
        self.encrypt_button.clicked.connect(self.encrypt_pdf)
        button_layout.addWidget(self.encrypt_button)
        
        self.layout.addLayout(button_layout)
        
        # 添加进度条和状态标签
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.status_label)
        
        # 添加底部空白
        self.layout.addStretch()
        
    def toggle_permissions(self, checked):
        """切换权限设置的启用状态"""
        for check in [self.print_check, self.modify_check, 
                     self.copy_check, self.annotate_check]:
            check.setEnabled(checked)
            
    def select_input_file(self):
        """选择输入文件"""
        file_name = self.select_file("选择要加密的PDF文件")
        if file_name:
            self.input_edit.setText(file_name)
            # 自动设置输出文件名
            dir_name = os.path.dirname(file_name)
            base_name = os.path.splitext(os.path.basename(file_name))[0]
            output_file = os.path.join(dir_name, f"{base_name}_encrypted.pdf")
            self.output_edit.setText(output_file)
            
    def select_output_file(self):
        """选择输出文件"""
        file_name = self.save_file("保存加密后的PDF文件")
        if file_name:
            self.output_edit.setText(file_name)
            
    def encrypt_pdf(self):
        """加密PDF文件"""
        input_file = self.input_edit.text()
        output_file = self.output_edit.text()
        
        if not input_file:
            QMessageBox.warning(self, "警告", "请选择要加密的PDF文件")
            return
            
        if not output_file:
            QMessageBox.warning(self, "警告", "请选择输出文件位置")
            return
            
        if not self.user_pwd_check.isChecked() and not self.owner_pwd_check.isChecked():
            QMessageBox.warning(self, "警告", "请至少设置一个密码")
            return
            
        try:
            from tools.pdf_encrypt import pdf_encrypt
            
            # 显示进度条
            self.progress.setMaximum(100)
            self.progress.setValue(0)
            self.progress.show()
            
            # 获取密码
            user_pwd = self.user_pwd_edit.text() if self.user_pwd_check.isChecked() else None
            owner_pwd = self.owner_pwd_edit.text() if self.owner_pwd_check.isChecked() else None
            
            # 获取权限设置
            permissions = {
                'print': self.print_check.isChecked(),
                'modify': self.modify_check.isChecked(),
                'copy': self.copy_check.isChecked(),
                'annotate': self.annotate_check.isChecked()
            }
            
            # 调用加密函数
            pdf_encrypt(input_file, output_file, user_pwd, owner_pwd, permissions)
            
            self.progress.setValue(100)
            self.show_message("PDF加密完成！")
            
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