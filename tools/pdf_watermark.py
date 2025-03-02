from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import math

def pdf_watermark(input_file, output_file, text, font_size=36, opacity=0.3):
    """
    为PDF添加水印
    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    :param text: 水印文本
    :param font_size: 字体大小
    :param opacity: 不透明度 (0-1)
    """
    # 创建临时水印PDF
    watermark_file = "temp_watermark.pdf"
    
    # 获取输入PDF的第一页尺寸
    reader = PdfReader(input_file)
    first_page = reader.pages[0]
    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)
    
    try:
        # 创建水印PDF
        c = canvas.Canvas(watermark_file)
        c.setPageSize((page_width, page_height))
        
        # 设置字体 - 优先使用中文字体
        font_found = False
        chinese_fonts = [
            ("/System/Library/Fonts/STHeiti Light.ttc", "STHeiti"),  # macOS
            ("/System/Library/Fonts/PingFang.ttc", "PingFang"),      # macOS
            ("C:\\Windows\\Fonts\\simhei.ttf", "SimHei"),           # Windows
            ("C:\\Windows\\Fonts\\msyh.ttf", "MicrosoftYaHei"),     # Windows
            ("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", "DroidSansFallback")  # Linux
        ]
        
        for font_path, font_name in chinese_fonts:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    c.setFont(font_name, font_size)
                    font_found = True
                    break
                except:
                    continue
        
        if not font_found:
            c.setFont('Helvetica', font_size)
        
        # 设置透明度
        c.setFillAlpha(opacity)
        
        # 计算水印文本大小
        text_width = c.stringWidth(text)
        text_height = font_size
        
        # 计算水印之间的间距
        x_spacing = text_width * 2
        y_spacing = text_height * 3
        
        # 计算倾斜角度
        angle = 30
        
        # 在整个页面上重复添加水印
        for y in range(-int(page_height), int(page_height*2), int(y_spacing)):
            for x in range(-int(page_width), int(page_width*2), int(x_spacing)):
                # 保存当前图形状态
                c.saveState()
                # 移动到指定位置
                c.translate(x, y)
                # 旋转
                c.rotate(angle)
                # 绘制文字
                c.drawString(0, 0, text)
                # 恢复图形状态
                c.restoreState()
        
        c.save()
        
        # 将水印应用到每一页
        writer = PdfWriter()
        watermark = PdfReader(watermark_file)
        watermark_page = watermark.pages[0]
        
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)
        
        # 保存结果
        with open(output_file, 'wb') as output:
            writer.write(output)
            
    finally:
        # 清理临时文件
        if os.path.exists(watermark_file):
            os.remove(watermark_file)