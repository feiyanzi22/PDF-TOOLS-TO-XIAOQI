import os
from PIL import Image
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def natural_sort_key(s):
    # 将字符串中的数字部分转换为整数进行比较
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def image_to_pdf(image_files, output_file):
    """
    将图片转换为PDF
    :param image_files: 图片文件路径列表
    :param output_file: 输出PDF文件路径
    """
    # 创建第一个图片对象
    first_image = Image.open(image_files[0])
    
    # 打开其他图片
    other_images = []
    for image_path in image_files[1:]:
        img = Image.open(image_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        other_images.append(img)
    
    # 如果第一张图片是RGBA模式，转换为RGB
    if first_image.mode == 'RGBA':
        first_image = first_image.convert('RGB')
    
    # 保存为PDF
    first_image.save(output_file, "PDF", save_all=True, append_images=other_images)

def image_to_pdf_from_folder():
    try:
        image_folder = input("请输入包含图片的文件夹路径：").strip().strip("'\"")
        output = input("请输入输出的 PDF 文件路径（比如 images.pdf）：").strip().strip("'\"")
        
        if not os.path.exists(image_folder):
            print(f"错误：文件夹 '{image_folder}' 不存在")
            return
            
        # 获取所有图片并按自然顺序排序
        images = [f for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        images.sort(key=natural_sort_key)  # 使用自然排序
        
        if not images:
            print("错误：文件夹中没有找到图片文件")
            return
            
        print(f"找到以下图片文件，将按此顺序合并：")
        for i, img in enumerate(images, 1):
            print(f"{i}. {img}")
            
        image_list = []
        # 转换所有图片
        for img_name in images:
            img_path = os.path.join(image_folder, img_name)
            image = Image.open(img_path)
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            image_list.append(image)
            
        # 保存PDF
        if image_list:
            image_to_pdf(image_list, output)
            print("图片转 PDF 完成！")
        
    except Exception as e:
        print(f"发生错误: {e}")