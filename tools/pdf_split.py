import os
from PyPDF2 import PdfReader, PdfWriter
import math

def pdf_split(input_file, output_dir, pages_per_file=None, num_files=None):
    """
    拆分PDF文件
    :param input_file: 输入文件路径
    :param output_dir: 输出目录
    :param pages_per_file: 每个文件的页数（按页数拆分时使用）
    :param num_files: 要拆分的文件数（按文件数拆分时使用）
    """
    # 打开PDF文件
    reader = PdfReader(input_file)
    total_pages = len(reader.pages)
    
    if pages_per_file:
        # 按页数拆分
        num_files = math.ceil(total_pages / pages_per_file)
        pages_per_file = [pages_per_file] * (num_files - 1)
        # 最后一个文件可能页数不足
        pages_per_file.append(total_pages - sum(pages_per_file))
    else:
        # 按文件数平均拆分
        base_pages = total_pages // num_files
        extra_pages = total_pages % num_files
        pages_per_file = [base_pages] * num_files
        # 将剩余页面分配给前几个文件
        for i in range(extra_pages):
            pages_per_file[i] += 1
    
    # 获取输入文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # 开始拆分
    current_page = 0
    for i, num_pages in enumerate(pages_per_file, 1):
        writer = PdfWriter()
        
        # 添加页面到新文件
        for j in range(num_pages):
            writer.add_page(reader.pages[current_page + j])
        
        # 保存拆分后的文件
        output_file = os.path.join(output_dir, f"{base_name}_part{i}.pdf")
        with open(output_file, "wb") as output:
            writer.write(output)
        
        current_page += num_pages