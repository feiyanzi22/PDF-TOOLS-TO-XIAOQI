from PyPDF2 import PdfReader, PdfWriter
import fitz  # PyMuPDF
import os
import numpy as np
from PIL import Image
import io
from scipy.ndimage import gaussian_filter, binary_dilation

def pdf_remove_watermark():
    try:
        input_file = input("请输入要处理的 PDF 文件路径：").strip().strip("'\"")
        output_file = input("请输入输出文件路径（比如 cleaned.pdf）：").strip().strip("'\"")
        
        # 打开PDF文件
        doc = fitz.open(input_file)
        output_doc = fitz.open()
        
        print("正在处理中，这可能需要一些时间...")
        
        # 处理每一页
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x放大以提高精度
            
            # 转换为PIL图像进行处理
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_array = np.array(img)
            
            # 检测灰色水印
            r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
            
            # 计算颜色的标准差（用于检测灰色）
            color_std = np.std([r, g, b], axis=0)
            
            # 检测灰色区域（RGB值非常接近）
            is_gray = color_std < 5
            
            # 计算亮度
            brightness = (r + g + b) / 3
            
            # 检测中等亮度的区域（对应半透明水印）
            is_medium = (brightness > 180) & (brightness < 250)
            
            # 组合条件找到水印
            watermark_mask = is_gray & is_medium
            
            # 使用形态学操作改进掩码
            # 首先进行腐蚀操作，去除小的误检区域
            from scipy.ndimage import binary_erosion
            watermark_mask = binary_erosion(watermark_mask, iterations=1)
            
            # 然后进行膨胀操作，恢复并略微扩展水印区域
            watermark_mask = binary_dilation(watermark_mask, iterations=2)
            
            # 创建结果图像
            result = img_array.copy()
            
            # 对水印区域进行处理
            for i in range(3):
                # 将水印区域的颜色设为纯白
                result[watermark_mask, i] = 255
            
            # 转回PIL图像
            cleaned_img = Image.fromarray(result.astype(np.uint8))
            
            # 创建新页面
            new_page = output_doc.new_page(width=page.rect.width,
                                         height=page.rect.height)
            
            # 将处理后的图像转换为PDF页面
            img_bytes = io.BytesIO()
            cleaned_img.save(img_bytes, format='PNG', optimize=True, quality=100)
            new_page.insert_image(new_page.rect, stream=img_bytes.getvalue())
            
            print(f"已处理第 {page_num + 1} 页")
        
        # 保存结果
        output_doc.save(output_file)
        output_doc.close()
        doc.close()
        
        print("水印去除完成！")
        print("注意：")
        print("1. 处理后的文件可能会比原文件大")
        print("2. 如果水印仍然可见，可以调整代码中的亮度阈值(180-250)")
        print("3. 如果文字受到影响，可以调整颜色标准差阈值(5)")
        
    except Exception as e:
        print(f"发生错误: {e}")
        print("\n可能的解决方案：")
        print("1. 确保安装了所需的库：pip install PyMuPDF numpy Pillow scipy")
        print("2. 确保PDF文件没有被加密")
        print("3. 确保有足够的磁盘空间") 