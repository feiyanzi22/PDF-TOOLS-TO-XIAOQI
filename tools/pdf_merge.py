import os
import re
from PyPDF2 import PdfReader, PdfWriter

def natural_sort_key(s):
    # 将字符串中的数字部分转换为整数进行比较
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def pdf_merge(input_files, output):
    """
    合并PDF文件
    :param input_files: PDF文件路径列表
    :param output: 输出文件路径
    """
    try:
        # 验证输入文件
        for pdf_file in input_files:
            if not os.path.exists(pdf_file):
                raise FileNotFoundError(f"文件不存在: {pdf_file}")
            if not pdf_file.lower().endswith('.pdf'):
                raise ValueError(f"不是PDF文件: {pdf_file}")
        
        # 创建PDF合并器
        merger = PdfWriter()
        
        # 按顺序合并PDF
        for pdf_file in input_files:
            merger.append(PdfReader(pdf_file))
        
        # 保存合并后的文件
        with open(output, "wb") as output_file:
            merger.write(output_file)
        
        return True
        
    except Exception as e:
        raise Exception(f"PDF合并失败: {str(e)}")