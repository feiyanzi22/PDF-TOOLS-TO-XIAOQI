import fitz  # PyMuPDF
import os

def pdf_to_image(input_file, output_dir, format='png', dpi=300, all_pages=True):
    """
    将PDF转换为图片
    :param input_file: 输入PDF文件路径
    :param output_dir: 输出目录
    :param format: 图片格式 (png/jpeg/bmp/tiff)
    :param dpi: 图片DPI
    :param all_pages: 是否转换所有页面
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 打开PDF文件
    pdf = fitz.open(input_file)
    
    # 计算缩放因子
    zoom = dpi / 72  # 72 is the default PDF DPI
    
    # 转换页面
    pages = range(len(pdf)) if all_pages else [0]
    for page_num in pages:
        page = pdf[page_num]
        
        # 获取页面像素图
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        
        # 生成输出文件名
        output_file = os.path.join(
            output_dir, 
            f"page_{page_num + 1}.{format}"
        )
        
        # 保存图片
        pix.save(output_file)
            
    # 关闭PDF
    pdf.close()