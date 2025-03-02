import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFileDialog,
                            QMessageBox, QLineEdit)
from PyQt6.QtCore import Qt
from tools.pdf_merge import pdf_merge
from tools.pdf_split import pdf_split
from tools.pdf_encrypt import pdf_encrypt
from tools.pdf_decrypt import pdf_decrypt
from tools.pdf_watermark import pdf_watermark
from tools.pdf_to_word import pdf_to_word
from tools.pdf_to_md import pdf_to_md
from tools.pdf_to_image import pdf_to_image
from tools.image_to_pdf import image_to_pdf
from tools.pdf_remove_watermark import pdf_remove_watermark
from pages.merge_page import MergePage
from pages.split_page import SplitPage
from pages.encrypt_page import EncryptPage
from pages.decrypt_page import DecryptPage
from pages.watermark_page import WatermarkPage  # 添加导入
from pages.to_image_page import ToImagePage  # 添加导入
from pages.to_pdf_page import ToPdfPage  # 添加导入
from styles.style import get_main_style, get_sidebar_style

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 工具箱")
        self.setMinimumSize(1000, 700)
        
        # 应用样式
        self.setStyleSheet(get_main_style())
        
        # 创建主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建侧边栏
        self.create_sidebar(layout)
        
        # 创建主内容区
        self.create_main_content(layout)
        
        # 初始化所有功能页面
        self.init_pages()
        
        # 默认显示第一个功能页面
        if self.button_group:
            self.button_group[0].setChecked(True)
            self.show_merge()
        
    def create_sidebar(self, layout):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet(get_sidebar_style())
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # 添加标题
        title = QLabel("PDF 工具箱")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)
        
        # 创建功能按钮
        self.create_sidebar_buttons(sidebar_layout)
        
        # 添加底部空白
        sidebar_layout.addStretch()
        layout.addWidget(sidebar)
        
    def create_sidebar_buttons(self, layout):
        self.button_group = []
        functions = [
            ("PDF 合并", self.show_merge),
            ("PDF 拆分", self.show_split),
            ("PDF 加密", self.show_encrypt),
            ("PDF 解密", self.show_decrypt),
            ("PDF 加水印", self.show_watermark),
            ("PDF 去水印", self.show_remove_watermark),
            ("PDF 转 Word", self.show_to_word),
            ("PDF 转 Markdown", self.show_to_md),
            ("PDF 转图片", self.show_to_image),
            ("图片转 PDF", self.show_to_pdf)
        ]
        
        for text, slot in functions:
            btn = QPushButton(text)
            btn.setObjectName("sidebar_button")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, b=btn, s=slot: self.handle_button_click(b, s))
            layout.addWidget(btn)
            self.button_group.append(btn)
    
    def create_main_content(self, layout):
        # 创建主内容区
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建功能页面堆栈
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        
        layout.addWidget(content)
        
    def init_pages(self):
        """初始化所有功能页面"""
        self.merge_page = MergePage()
        self.split_page = SplitPage()
        self.encrypt_page = EncryptPage()
        self.decrypt_page = DecryptPage()
        self.watermark_page = WatermarkPage()
        self.to_image_page = ToImagePage()  # 添加转图片页面
        self.to_pdf_page = ToPdfPage()  # 添加图片转PDF页面
        self.stack.addWidget(self.merge_page)
        self.stack.addWidget(self.split_page)
        self.stack.addWidget(self.encrypt_page)
        self.stack.addWidget(self.decrypt_page)
        self.stack.addWidget(self.watermark_page)
        self.stack.addWidget(self.to_image_page)  # 添加到堆栈
        self.stack.addWidget(self.to_pdf_page)  # 添加到堆栈
        # 后续会添加其他页面
        
    def handle_button_click(self, clicked_button, slot):
        """处理侧边栏按钮点击"""
        # 取消其他按钮的选中状态
        for btn in self.button_group:
            if btn != clicked_button:
                btn.setChecked(False)
        
        # 调用对应的功能
        slot()

    def show_merge(self):
        """显示 PDF 合并页面"""
        self.stack.setCurrentWidget(self.merge_page)
        
    def show_split(self):
        """显示 PDF 拆分页面"""
        self.stack.setCurrentWidget(self.split_page)
        
    def show_encrypt(self):
        """显示 PDF 加密页面"""
        self.stack.setCurrentWidget(self.encrypt_page)
        
    def show_decrypt(self):
        """显示 PDF 解密页面"""
        self.stack.setCurrentWidget(self.decrypt_page)
        
    def show_watermark(self):
        """显示 PDF 加水印页面"""
        self.stack.setCurrentWidget(self.watermark_page)
        
    def show_remove_watermark(self):
        """显示 PDF 去水印页面"""
        QMessageBox.information(self, "提示", "PDF去水印功能正在开发中")
        
    def show_to_word(self):
        """显示 PDF 转 Word 页面"""
        QMessageBox.information(self, "提示", "PDF转Word功能正在开发中")
        
    def show_to_md(self):
        """显示 PDF 转 Markdown 页面"""
        QMessageBox.information(self, "提示", "PDF转Markdown功能正在开发中")
        
    def show_to_image(self):
        """显示 PDF 转图片页面"""
        self.stack.setCurrentWidget(self.to_image_page)
        
    def show_to_pdf(self):
        """显示图片转 PDF 页面"""
        self.stack.setCurrentWidget(self.to_pdf_page)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
