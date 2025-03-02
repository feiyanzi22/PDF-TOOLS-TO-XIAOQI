import os
import sys
import platform

def create_shortcut():
    try:
        # 检测操作系统
        if platform.system() == "Darwin":  # macOS
            # 获取应用程序路径
            app_path = os.path.abspath("app.py")
            python_path = sys.executable
            
            # 创建 .command 文件
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            command_path = os.path.join(desktop, "PDF工具.command")
            
            # 写入启动脚本
            with open(command_path, "w") as f:
                f.write(f'#!/bin/bash\n')
                f.write(f'cd "{os.path.dirname(app_path)}"\n')
                f.write(f'"{python_path}" "{app_path}"\n')
            
            # 设置可执行权限
            os.chmod(command_path, 0o755)
            
            print("桌面快捷方式创建成功！")
            
        else:  # Windows
            from win32com.client import Dispatch
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            app_path = os.path.abspath("app.py")
            python_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
            
            shortcut_path = os.path.join(desktop, "PDF工具.lnk")
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = python_path
            shortcut.Arguments = f'"{app_path}"'
            shortcut.WorkingDirectory = os.path.dirname(app_path)
            
            icon_path = os.path.abspath("icon.ico")
            if os.path.exists(icon_path):
                shortcut.IconLocation = icon_path
                
            shortcut.save()
            print("桌面快捷方式创建成功！")
            
    except Exception as e:
        print(f"创建快捷方式时出错：{str(e)}")
        input("按回车键退出...")

if __name__ == "__main__":
    create_shortcut() 