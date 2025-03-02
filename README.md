# PDF 工具箱

一个基于 PyQt6 的 PDF 工具箱应用程序，提供 PDF 合并等功能。

## 功能特点

- PDF 文件合并
- 支持拖拽排序
- 支持列表/图标两种视图模式
- 支持文件预览
- 支持批量添加

## 安装说明

1. 确保已安装 Python 3.8 或更高版本
2. 克隆或下载本项目
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 直接运行：
   ```bash
   python app.py
   ```

2. 创建桌面快捷方式：
   - Windows: 运行 `create_shortcut.bat` 或 `python create_shortcut.py`
   - macOS: 运行 `python create_shortcut.py`

## 使用说明

1. 添加文件：
   - 点击"添加文件"选择单个或多个PDF文件
   - 点击"添加文件夹"选择整个文件夹
   - 拖拽文件到程序窗口

2. 管理文件：
   - 拖拽调整文件顺序
   - 右键菜单可删除文件
   - 支持按名称或时间排序

3. 视图切换：
   - 列表视图：显示完整文件路径
   - 图标视图：显示文件预览和文件名

4. 合并文件：
   - 调整好顺序后点击"合并PDF"
   - 选择保存位置即可完成合并

## 系统要求

- Windows 7 或更高版本
- macOS 10.12 或更高版本
- Python 3.8+

## 注意事项

- 请确保有足够的磁盘空间
- 大文件处理可能需要较长时间
- 建议定期清理临时文件


## 更新日志
V1.0.0 初始版本，2025年03月02日，Grok 3、Cursor、Claude 3.5 Sonnet，PDF转word和md以及PDF去水印还没有开发完成。飞烟子

## 许可证

MIT License 