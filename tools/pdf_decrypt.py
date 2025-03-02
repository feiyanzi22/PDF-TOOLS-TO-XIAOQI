from PyPDF2 import PdfReader, PdfWriter

def pdf_decrypt(input_file, output_file, password):
    """
    解密PDF文件
    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    :param password: 密码
    """
    # 读取PDF文件
    reader = PdfReader(input_file)
    
    # 尝试解密
    if reader.is_encrypted:
        try:
            reader.decrypt(password)
        except:
            raise Exception("密码错误或PDF文件已损坏")
    
    # 创建新的PDF写入器
    writer = PdfWriter()
    
    # 复制所有页面
    for page in reader.pages:
        writer.add_page(page)
    
    # 保存解密后的文件
    with open(output_file, 'wb') as output:
        writer.write(output)