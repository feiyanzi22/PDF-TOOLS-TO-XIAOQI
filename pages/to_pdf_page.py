from .base_page import BasePage
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QLineEdit, QGridLayout, QFrame, QMessageBox,
                            QListWidget, QListWidgetItem, QMenu, QListView)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from styles.style import get_page_style
import os
import re

def natural_sort_key(s):
    """自然排序的键函数"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

class DraggableImageList(QListWidget):
    def __init__(self):
        super().__init__()
        # 基本拖放设置
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setDropIndicatorShown(True)
        
        # 右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # 设置图标大小
        self.setIconSize(QSize(80, 80))
        self.setGridSize(QSize(100, 120))
        
        # 设置视图模式
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setMovement(QListView.Movement.Free)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setSpacing(10)
        self.setWrapping(True)
        
        # 设置样式
        self.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            QListWidget::item {
                color: #333333;
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                border: 1px solid #2196F3;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)
        
    def add_image_item(self, image_path):
        """添加图片项"""
        # 创建缩略图
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, 
                                 Qt.TransformationMode.SmoothTransformation)
            icon = QIcon(pixmap)
            
            # 创建列表项
            item = QListWidgetItem(icon, os.path.basename(image_path))
            item.setData(Qt.ItemDataRole.UserRole, image_path)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.addItem(item)
            
    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu()
        
        # 添加排序子菜单
        sort_menu = menu.addMenu("排序方式")
        
        # 添加各种排序方式
        natural_sort_action = sort_menu.addAction("自然排序")
        natural_sort_action.triggered.connect(lambda: self.sort_items("natural"))
        
        # 名称排序子菜单
        name_menu = sort_menu.addMenu("名称排序")
        name_asc_action = name_menu.addAction("升序")
        name_asc_action.triggered.connect(lambda: self.sort_items("name_asc"))
        name_desc_action = name_menu.addAction("降序")
        name_desc_action.triggered.connect(lambda: self.sort_items("name_desc"))
        
        # 时间排序子菜单
        time_menu = sort_menu.addMenu("创建时间")
        time_asc_action = time_menu.addAction("升序")
        time_asc_action.triggered.connect(lambda: self.sort_items("time_asc"))
        time_desc_action = time_menu.addAction("降序")
        time_desc_action.triggered.connect(lambda: self.sort_items("time_desc"))
        
        # 添加分隔线
        menu.addSeparator()
        
        # 添加删除选项
        remove_action = menu.addAction("删除")
        remove_action.triggered.connect(self.remove_selected_items)
        
        if self.count() > 0:  # 只有在列表非空时显示菜单
            menu.exec(self.mapToGlobal(position))
            
    def sort_items(self, sort_type):
        """排序列表项
        :param sort_type: 排序类型，可选值：natural, name_asc, name_desc, time_asc, time_desc
        """
        items = []
        # 保存所有项
        for i in range(self.count()):
            item = self.takeItem(0)  # 总是取第一个项，因为取出后列表会自动调整
            items.append(item)
        
        # 根据不同的排序方式进行排序
        if sort_type == "natural":
            items.sort(key=lambda x: natural_sort_key(x.text()))
        elif sort_type == "name_asc":
            items.sort(key=lambda x: x.text().lower())
        elif sort_type == "name_desc":
            items.sort(key=lambda x: x.text().lower(), reverse=True)
        elif sort_type == "time_asc":
            items.sort(key=lambda x: os.path.getctime(x.data(Qt.ItemDataRole.UserRole)))
        elif sort_type == "time_desc":
            items.sort(key=lambda x: os.path.getctime(x.data(Qt.ItemDataRole.UserRole)), reverse=True)
        
        # 重新添加排序后的项
        for item in items:
            self.addItem(item)
            
    def remove_selected_items(self):
        """删除选中的项目"""
        for item in self.selectedItems():
            self.takeItem(self.row(item))

class ToPdfPage(BasePage):
    def __init__(self):
        super().__init__("图片转 PDF")
        
        # 设置样式
        self.setStyleSheet(get_page_style())
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # 添加文件按钮
        add_button = QPushButton("添加图片")
        add_button.clicked.connect(self.add_files)
        button_layout.addWidget(add_button)
        
        # 添加文件夹按钮
        add_folder_button = QPushButton("添加文件夹")
        add_folder_button.clicked.connect(self.add_folder)
        button_layout.addWidget(add_folder_button)
        
        # 清空列表按钮
        clear_button = QPushButton("清空列表")
        clear_button.clicked.connect(self.clear_list)
        button_layout.addWidget(clear_button)
        
        # 转换按钮
        convert_button = QPushButton("转换为PDF")
        convert_button.clicked.connect(self.convert_to_pdf)
        button_layout.addWidget(convert_button)
        
        self.layout.addLayout(button_layout)
        
        # 文件列表区域
        list_frame = QFrame()
        list_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        list_layout = QVBoxLayout(list_frame)
        
        # 创建文件列表
        self.file_list = DraggableImageList()
        list_layout.addWidget(self.file_list)
        
        self.layout.addWidget(list_frame)
        
        # 添加进度条和状态标签
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.status_label)
        
        # 设置按钮样式
        button_style = """
            QPushButton {
                min-width: 120px;
                padding: 8px 16px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """
        add_button.setStyleSheet(button_style)
        add_folder_button.setStyleSheet(button_style)
        clear_button.setStyleSheet(button_style)
        convert_button.setStyleSheet(button_style)
        
    def add_files(self):
        """添加图片文件"""
        files = self.select_files("选择图片文件", "图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff)")
        if files:
            # 对文件进行自然排序
            files = sorted(files, key=natural_sort_key)
            for file in files:
                self.file_list.add_image_item(file)
                
    def add_folder(self):
        """添加文件夹中的所有图片"""
        folder = self.select_folder()
        if folder:
            image_files = []
            for f in os.listdir(folder):
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                    image_files.append(os.path.join(folder, f))
            
            if image_files:
                # 对文件进行自然排序
                image_files.sort(key=natural_sort_key)
                for file in image_files:
                    self.file_list.add_image_item(file)
            else:
                QMessageBox.warning(self, "警告", "所选文件夹中没有支持的图片文件")
                
    def clear_list(self):
        """清空文件列表"""
        self.file_list.clear()
        
    def convert_to_pdf(self):
        """转换为PDF"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加图片文件")
            return
            
        output_file = self.save_file("保存PDF文件", "PDF文件 (*.pdf)")
        if not output_file:
            return
            
        try:
            # 获取所有图片路径（按当前列表顺序）
            image_files = []
            for i in range(self.file_list.count()):
                item = self.file_list.item(i)
                image_files.append(item.data(Qt.ItemDataRole.UserRole))
            
            # 显示进度条
            self.progress.setMaximum(len(image_files))
            self.progress.setValue(0)
            self.progress.show()
            
            # 调用转换函数
            from tools.image_to_pdf import image_to_pdf
            image_to_pdf(image_files, output_file)
            
            self.progress.setValue(len(image_files))
            self.show_message("转换完成！")
            
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