from .base_page import BasePage
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QListWidget, QMessageBox, QListWidgetItem,
                            QMenu, QListView, QButtonGroup, QRadioButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon
import os
import re
import fitz  # PyMuPDF，用于生成PDF预览

def natural_sort_key(s):
    """自然排序的键函数"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

class DraggableListWidget(QListWidget):
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
        
        # 设置移动模式
        self.setMovement(QListView.Movement.Snap)
        
        # 设置调整大小模式
        self.setResizeMode(QListView.ResizeMode.Adjust)
        
        # 设置布局模式
        self.setLayoutMode(QListView.LayoutMode.SinglePass)
        
        # 跟踪当前视图模式
        self._is_icon_mode = False
        
        # 设置基本样式
        self.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            QListWidget::item {
                color: black;  /* 设置文字颜色为黑色 */
                background-color: transparent;
                border-bottom: 1px solid #f0f0f0;
                padding: 4px 8px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                border: 1px solid #2196F3;
                color: black;  /* 确保选中时也是黑色 */
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
                color: black;  /* 确保悬停时也是黑色 */
            }
        """)
        
    def setViewMode(self, mode):
        """重写设置视图模式的方法"""
        super().setViewMode(mode)
        self._is_icon_mode = (mode == QListView.ViewMode.IconMode)
        
        # 根据视图模式调整设置
        if self._is_icon_mode:
            self.setMovement(QListView.Movement.Snap)
            self.setResizeMode(QListView.ResizeMode.Adjust)
            self.setSpacing(10)
            self.setGridSize(QSize(100, 120))
            self.setFlow(QListView.Flow.LeftToRight)
            self.setWrapping(True)
        else:
            self.setMovement(QListView.Movement.Snap)
            self.setResizeMode(QListView.ResizeMode.Fixed)
            self.setSpacing(2)
            self.setGridSize(QSize(0, 25))
            self.setFlow(QListView.Flow.TopToBottom)
            self.setWrapping(False)

    def dragEnterEvent(self, event):
        if event.source() == self:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.source() == self:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.source() != self:
            event.ignore()
            return

        # 调用父类的默认处理
        super().dropEvent(event)

    def show_context_menu(self, position):
        menu = QMenu()
        
        # 删除操作
        delete_action = menu.addAction("删除选中项")
        delete_action.triggered.connect(self.delete_selected_items)
        
        # 排序子菜单
        sort_menu = menu.addMenu("排序方式")
        
        # 按文件名排序
        name_menu = sort_menu.addMenu("按文件名排序")
        name_natural = name_menu.addAction("自然排序")
        name_asc = name_menu.addAction("字母升序")
        name_desc = name_menu.addAction("字母降序")
        name_natural.triggered.connect(lambda: self.sort_items("natural", True))
        name_asc.triggered.connect(lambda: self.sort_items("name", True))
        name_desc.triggered.connect(lambda: self.sort_items("name", False))
        
        # 按修改时间排序
        time_menu = sort_menu.addMenu("按修改时间排序")
        time_asc = time_menu.addAction("从旧到新")
        time_desc = time_menu.addAction("从新到旧")
        time_asc.triggered.connect(lambda: self.sort_items("time", True))
        time_desc.triggered.connect(lambda: self.sort_items("time", False))
        
        menu.exec(self.mapToGlobal(position))
        
    def delete_selected_items(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))
            
    def sort_items(self, key="name", ascending=True):
        """排序列表项"""
        # 禁用排序以防止自动排序
        self.setSortingEnabled(False)
        
        # 收集所有项目及其数据
        items_data = []
        while self.count() > 0:
            item = self.takeItem(0)
            items_data.append({
                'text': item.text(),
                'icon': item.icon(),
                'tooltip': item.toolTip(),
                'data': item.data(Qt.ItemDataRole.UserRole),
                'flags': item.flags(),
                'selected': item.isSelected()
            })
        
        # 根据不同的排序方式进行排序
        if key == "natural":
            items_data.sort(key=lambda x: natural_sort_key(x['text']))
        elif key == "name":
            items_data.sort(key=lambda x: x['text'].lower(), 
                          reverse=not ascending)
        else:  # time
            items_data.sort(key=lambda x: os.path.getmtime(x['data']), 
                          reverse=not ascending)
        
        # 重新添加排序后的项目
        for data in items_data:
            item = QListWidgetItem()
            item.setText(data['text'])
            item.setIcon(data['icon'])
            item.setToolTip(data['tooltip'])
            item.setData(Qt.ItemDataRole.UserRole, data['data'])
            item.setFlags(data['flags'])
            self.addItem(item)
            item.setSelected(data['selected'])
            
    def get_pdf_preview(self, pdf_path):
        """获取PDF第一页的预览图标"""
        try:
            doc = fitz.open(pdf_path)
            if doc.page_count > 0:
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))  # 缩小尺寸
                img_path = os.path.join(os.path.dirname(pdf_path), 
                                      f".preview_{os.path.basename(pdf_path)}.png")
                pix.save(img_path)
                doc.close()
                return QIcon(img_path)
        except Exception:
            pass
        return QIcon.fromTheme("application-pdf")  # 使用默认PDF图标
            
    def add_file_item(self, file_path):
        """添加一个文件项到列表"""
        item = QListWidgetItem(os.path.basename(file_path))  # 只显示文件名
        item.setToolTip(file_path)  # 完整路径显示在工具提示中
        item.setData(Qt.ItemDataRole.UserRole, file_path)  # 存储完整路径
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        
        # 设置图标
        icon = self.get_pdf_preview(file_path)
        item.setIcon(icon)
        
        # 强制设置文本颜色为黑色
        item.setForeground(Qt.GlobalColor.black)
        
        self.addItem(item)
    
    def add_files(self):
        """添加PDF文件"""
        files = self.select_files()
        if files:
            # 对文件进行自然排序
            files = sorted(files, key=natural_sort_key)
            for file in files:
                self.add_file_item(file)
            
    def add_folder(self):
        """添加文件夹中的所有PDF文件"""
        folder = self.select_folder()
        if folder:
            pdf_files = [os.path.join(folder, f) for f in os.listdir(folder) 
                        if f.lower().endswith('.pdf')]
            if pdf_files:
                # 对文件进行自然排序
                pdf_files.sort(key=natural_sort_key)
                for file in pdf_files:
                    self.add_file_item(file)
            else:
                QMessageBox.warning(self, "警告", "所选文件夹中没有PDF文件")
    
    def clear_list(self):
        """清空文件列表"""
        self.clear()
        
    def merge_pdfs(self):
        """合并PDF文件"""
        if self.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加PDF文件")
            return
            
        output_file = self.save_file()
        if not output_file:
            return
            
        try:
            # 获取所有文件路径（按当前列表顺序）
            input_files = []
            for i in range(self.count()):
                item = self.item(i)
                input_files.append(item.data(Qt.ItemDataRole.UserRole))
            
            # 显示进度条
            self.progress.setMaximum(len(input_files))
            self.progress.setValue(0)
            self.progress.show()
            
            # 调用合并函数
            from tools.pdf_merge import pdf_merge
            pdf_merge(input_files=input_files, output=output_file)
            
            self.progress.setValue(len(input_files))
            self.show_message("PDF合并完成！")
            
        except Exception as e:
            self.show_message(f"发生错误: {str(e)}", True)
            QMessageBox.critical(self, "错误", str(e))
            
        finally:
            self.progress.hide() 

    def change_view(self, button):
        """切换视图模式"""
        if self.view_group.checkedId() == 0:  # 列表视图
            self.file_list.setViewMode(QListView.ViewMode.ListMode)
        else:  # 图标视图
            self.file_list.setViewMode(QListView.ViewMode.IconMode) 

class MergePage(BasePage):
    def __init__(self):
        super().__init__("PDF 合并")
        
        # 按钮布局 - 移到顶部
        button_layout = QHBoxLayout()
        
        # 添加文件按钮
        add_button = QPushButton("添加文件")
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
        
        # 合并按钮
        merge_button = QPushButton("合并PDF")
        merge_button.clicked.connect(self.merge_pdfs)
        button_layout.addWidget(merge_button)
        
        self.layout.addLayout(button_layout)
        
        # 视图切换按钮
        view_layout = QHBoxLayout()
        self.view_group = QButtonGroup()
        
        list_view_btn = QRadioButton("列表视图")
        list_view_btn.setChecked(True)
        icon_view_btn = QRadioButton("图标视图")
        
        self.view_group.addButton(list_view_btn, 0)
        self.view_group.addButton(icon_view_btn, 1)
        self.view_group.buttonClicked.connect(self.change_view)
        
        view_layout.addWidget(list_view_btn)
        view_layout.addWidget(icon_view_btn)
        view_layout.addStretch()
        self.layout.addLayout(view_layout)
        
        # 文件列表说明
        list_label = QLabel("拖动文件可以调整顺序，右键点击可以删除文件")
        list_label.setStyleSheet("color: gray;")
        self.layout.addWidget(list_label)
        
        # 文件列表
        self.file_list = DraggableListWidget()
        self.layout.addWidget(self.file_list)
        
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
        merge_button.setStyleSheet(button_style)
        
    def change_view(self, button):
        """切换视图模式"""
        if self.view_group.checkedId() == 0:  # 列表视图
            self.file_list.setViewMode(QListView.ViewMode.ListMode)
        else:  # 图标视图
            self.file_list.setViewMode(QListView.ViewMode.IconMode)
            
    def add_files(self):
        """添加PDF文件"""
        files = self.select_files()
        if files:
            # 对文件进行自然排序
            files = sorted(files, key=natural_sort_key)
            for file in files:
                self.file_list.add_file_item(file)
                
    def add_folder(self):
        """添加文件夹中的所有PDF文件"""
        folder = self.select_folder()
        if folder:
            pdf_files = [os.path.join(folder, f) for f in os.listdir(folder) 
                        if f.lower().endswith('.pdf')]
            if pdf_files:
                # 对文件进行自然排序
                pdf_files.sort(key=natural_sort_key)
                for file in pdf_files:
                    self.file_list.add_file_item(file)
            else:
                QMessageBox.warning(self, "警告", "所选文件夹中没有PDF文件")
                
    def clear_list(self):
        """清空文件列表"""
        self.file_list.clear()
        
    def merge_pdfs(self):
        """合并PDF文件"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加PDF文件")
            return
            
        output_file = self.save_file()
        if not output_file:
            return
            
        try:
            # 获取所有文件路径（按当前列表顺序）
            input_files = []
            for i in range(self.file_list.count()):
                item = self.file_list.item(i)
                input_files.append(item.data(Qt.ItemDataRole.UserRole))
            
            # 显示进度条
            self.progress.setMaximum(len(input_files))
            self.progress.setValue(0)
            self.progress.show()
            
            # 调用合并函数
            from tools.pdf_merge import pdf_merge
            pdf_merge(input_files=input_files, output=output_file)
            
            self.progress.setValue(len(input_files))
            self.show_message("PDF合并完成！")
            
        except Exception as e:
            self.show_message(f"发生错误: {str(e)}", True)
            QMessageBox.critical(self, "错误", str(e))
            
        finally:
            self.progress.hide() 