import os
import subprocess
import time
import shutil

def run_command(cmd):
    try:
        subprocess.run(cmd, check=False, capture_output=True)
        return True
    except:
        return False

def clean_dmg():
    print("开始清理...")
    
    # 获取所有磁盘信息
    result = subprocess.run(['diskutil', 'list'], capture_output=True, text=True)
    
    # 查找所有 PDF工具箱 相关的磁盘
    for line in result.stdout.split('\n'):
        if 'PDF工具箱' in line:
            # 提取磁盘标识符
            parts = line.split()
            disk_id = parts[-1]
            print(f"正在卸载 {disk_id}...")
            run_command(['diskutil', 'unmount', 'force', f'/dev/{disk_id}'])
            time.sleep(1)
    
    # 清理 dist 目录下的所有文件
    dist_path = 'dist'
    if os.path.exists(dist_path):
        print(f"清理 {dist_path} 目录...")
        try:
            # 删除整个 dist 目录
            shutil.rmtree(dist_path)
            print(f"{dist_path} 目录已清理")
        except Exception as e:
            print(f"清理 {dist_path} 时出错: {e}")
    
    # 清理其他临时文件和目录
    paths_to_clean = [
        'build',
        '__pycache__',
        '*.spec',
        '*.pyc',
        '.DS_Store'  # macOS 系统文件
    ]
    
    for path in paths_to_clean:
        try:
            if '*' in path:
                # 处理通配符模式
                import glob
                for p in glob.glob(path):
                    if os.path.isdir(p):
                        shutil.rmtree(p)
                    else:
                        os.remove(p)
                    print(f"删除: {p}")
            else:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    print(f"删除: {path}")
        except Exception as e:
            print(f"清理 {path} 时出错: {e}")
    
    print("清理完成")

if __name__ == "__main__":
    clean_dmg() 