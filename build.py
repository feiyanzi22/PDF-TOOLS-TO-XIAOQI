import os
import sys
import platform
from PyInstaller.__main__ import run

def build():
    # 基本配置
    opts = [
        'app.py',  # 主程序入口
        '--name=PDF工具箱',  # 应用名称
        '--noconsole',  # 不显示控制台
        '--windowed',  # 以窗口模式运行
        '--icon=icon.ico',  # 应用图标
        '--add-data=tools:tools',  # 包含tools目录
        '--add-data=pages:pages',  # 包含pages目录
        '--clean',  # 清理临时文件
    ]
    
    # 根据操作系统添加特定选项
    if platform.system() == "Darwin":  # macOS
        opts.extend([
            '--add-binary=/System/Library/Frameworks/Tk.framework/Tk:tk',
            '--add-binary=/System/Library/Frameworks/Tcl.framework/Tcl:tcl',
            '--codesign-identity=Developer ID Application',  # 如果有开发者证书
        ])
        
    elif platform.system() == "Windows":  # Windows
        opts.extend([
            '--add-binary=venv/Lib/site-packages/PyQt6/Qt6/bin/Qt6Core.dll:PyQt6/Qt6/bin',
            '--add-binary=venv/Lib/site-packages/PyQt6/Qt6/bin/Qt6Gui.dll:PyQt6/Qt6/bin',
            '--add-binary=venv/Lib/site-packages/PyQt6/Qt6/bin/Qt6Widgets.dll:PyQt6/Qt6/bin',
        ])
    
    # 运行打包命令
    run(opts)

if __name__ == "__main__":
    # 安装依赖
    os.system('pip install -r requirements.txt')
    # 安装PyInstaller
    os.system('pip install pyinstaller')
    # 开始打包
    build() 