import os
import subprocess
import time
from pathlib import Path

def run_command(cmd, desc=None, check=True, retries=3):
    """运行命令并支持重试"""
    for attempt in range(retries):
        if desc:
            print(f"{desc}... (尝试 {attempt + 1}/{retries})")
        try:
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"错误: {e.stderr}")
            if attempt < retries - 1:
                print("等待后重试...")
                time.sleep(3)
            continue
    return False

def force_unmount(volume_path):
    """强制卸载卷并等待"""
    attempts = 3
    while attempts > 0:
        print(f"尝试卸载 {volume_path}...")
        if run_command(["diskutil", "unmount", "force", volume_path], check=False):
            time.sleep(2)  # 等待系统完成卸载
            return True
        attempts -= 1
        time.sleep(2)
    return False

def create_dmg():
    try:
        # 应用名称
        app_name = "PDF工具箱"
        volume_path = f"/Volumes/{app_name}"
        
        # 获取路径
        current_dir = Path.cwd()
        dist_dir = current_dir / "dist"
        app_path = dist_dir / f"{app_name}.app"
        dmg_path = dist_dir / f"{app_name}.dmg"
        temp_dir = dist_dir / "temp_dmg"
        temp_dmg = dist_dir / "temp.dmg"
        
        # 确保 .app 文件存在
        if not app_path.exists():
            print(f"错误：找不到 {app_path}")
            return
            
        # 清理旧文件
        print("清理旧文件...")
        if os.path.exists(volume_path):
            force_unmount(volume_path)
        for path in [temp_dir, temp_dmg, dmg_path]:
            if path.exists():
                if path.is_dir():
                    os.system(f"rm -rf {path}")
                else:
                    os.remove(path)
                    
        # 创建临时目录
        print("准备临时文件...")
        temp_dir.mkdir(exist_ok=True)
        
        # 复制文件
        run_command(["cp", "-r", str(app_path), str(temp_dir)], "复制应用")
        run_command(["ln", "-s", "/Applications", str(temp_dir / "Applications")], "创建快捷方式")
        
        # 创建临时 DMG
        print("创建临时 DMG...")
        if not run_command([
            "hdiutil", "create",
            "-volname", app_name,
            "-srcfolder", str(temp_dir),
            "-ov",
            "-format", "UDRW",
            str(temp_dmg)
        ]):
            raise Exception("创建临时 DMG 失败")
            
        # 挂载 DMG
        print("挂载 DMG...")
        if not run_command([
            "hdiutil", "attach",
            str(temp_dmg),
            "-mountpoint", volume_path
        ]):
            raise Exception("挂载 DMG 失败")
            
        # 等待挂载
        time.sleep(3)
        
        # 设置窗口样式
        print("设置窗口样式...")
        run_command([
            "osascript", "-e",
            f'''
            tell application "Finder"
                tell disk "{app_name}"
                    open
                    set current view of container window to icon view
                    set toolbar visible of container window to false
                    set statusbar visible of container window to false
                    set bounds of container window to {100, 100, 700, 500}
                    set theViewOptions to the icon view options of container window
                    set arrangement of theViewOptions to not arranged
                    set icon size of theViewOptions to 128
                    set position of item "{app_name}.app" of container window to {150, 200}
                    set position of item "Applications" of container window to {550, 200}
                    close
                end tell
                delay 3
            end tell
            '''
        ])
        
        # 等待 Finder 完成
        time.sleep(5)
        
        # 卸载 DMG
        print("卸载 DMG...")
        if not force_unmount(volume_path):
            raise Exception("无法卸载 DMG")
            
        # 转换 DMG (添加重试机制)
        print("创建最终 DMG...")
        for attempt in range(3):
            print(f"尝试转换 DMG... (尝试 {attempt + 1}/3)")
            # 确保完全卸载
            force_unmount(volume_path)
            time.sleep(3)  # 多等待一会
            
            if run_command([
                "hdiutil", "convert",
                str(temp_dmg),
                "-format", "UDZO",
                "-o", str(dmg_path)
            ]):
                print("DMG 转换成功！")
                break
            else:
                if attempt < 2:
                    print("转换失败，等待后重试...")
                    time.sleep(5)
                else:
                    raise Exception("转换 DMG 失败")
            
        # 清理
        print("清理临时文件...")
        for path in [temp_dir, temp_dmg]:
            if path.exists():
                if path.is_dir():
                    os.system(f"rm -rf {path}")
                else:
                    os.remove(path)
                    
        print(f"DMG 文件创建成功：{dmg_path}")
        
    except Exception as e:
        print(f"错误：{str(e)}")
        # 清理
        try:
            if os.path.exists(volume_path):
                force_unmount(volume_path)
            for path in [temp_dir, temp_dmg]:
                if path.exists():
                    if path.is_dir():
                        os.system(f"rm -rf {path}")
                    else:
                        os.remove(path)
        except:
            pass
        raise

if __name__ == "__main__":
    create_dmg() 