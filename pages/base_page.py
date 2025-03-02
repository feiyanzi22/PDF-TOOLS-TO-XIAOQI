from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QFileDialog, QLineEdit, QProgressBar, QFrame)
from PyQt6.QtCore import Qt

class BasePage(QWidget):
    def __init__(self, title):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标题容器
        title_container = QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
            }
        """)
        title_layout = QVBoxLayout(title_container)
        
        # 页面标题
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: transparent;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.setContentsMargins(10, 5, 10, 5)
        
        # 添加标题容器到主布局
        self.layout.addWidget(title_container)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(line)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.hide()
        
        # 状态标签
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.hide()
        
    def show_message(self, message, is_error=False):
        """显示状态消息"""
        self.status_label.setText(message)
        if is_error:
            self.status_label.setStyleSheet("color: red;")
        else:
            self.status_label.setStyleSheet("color: green;")
        self.status_label.show()
        
    def select_file(self, title="选择文件", file_type="PDF Files (*.pdf)"):
        """选择文件对话框"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, title, "", file_type)
        return file_name
        
    def select_files(self, title="选择文件", file_type="PDF Files (*.pdf)"):
        """选择多个文件对话框"""
        files, _ = QFileDialog.getOpenFileNames(
            self, title, "", file_type)
        return files
        
    def select_folder(self, title="选择文件夹"):
        """选择文件夹对话框"""
        folder = QFileDialog.getExistingDirectory(
            self, title)
        return folder
        
    def save_file(self, title="保存文件", file_type="PDF Files (*.pdf)"):
        """保存文件对话框"""
        file_name, _ = QFileDialog.getSaveFileName(
            self, title, "", file_type)
        return file_name 