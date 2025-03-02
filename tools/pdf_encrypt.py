from PyPDF2 import PdfReader, PdfWriter

def pdf_encrypt(input_file, output_file, user_pwd=None, owner_pwd=None, permissions=None):
    """
    加密PDF文件
    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    :param user_pwd: 用户密码（打开密码）
    :param owner_pwd: 所有者密码（权限密码）
    :param permissions: 权限设置字典
    """
    # 读取PDF文件
    reader = PdfReader(input_file)
    writer = PdfWriter()
    
    # 复制所有页面
    for page in reader.pages:
        writer.add_page(page)
    
    # 设置加密
    if permissions:
        # 获取权限标志
        perm_flags = get_permission_flags(permissions)
        
        # 设置加密
        writer.encrypt(
            user_password=user_pwd if user_pwd else '',
            owner_password=owner_pwd if owner_pwd else (user_pwd if user_pwd else ''),
            use_128bit=True,
            permissions_flag=perm_flags
        )
    
    # 保存加密后的文件
    with open(output_file, 'wb') as output:
        writer.write(output)

def get_permission_flags(permissions):
    """
    根据权限设置获取权限标志
    :param permissions: 权限设置字典
    :return: 权限标志整数
    """
    flags = 0
    
    # 定义权限常量
    PRINT = 2048  # 打印权限
    MODIFY = 512  # 修改权限
    COPY = 16     # 复制权限
    ANNOTATE = 32 # 注释权限
    
    # 设置权限标志
    if permissions.get('print', True):
        flags |= PRINT
    if permissions.get('modify', True):
        flags |= MODIFY
    if permissions.get('copy', True):
        flags |= COPY
    if permissions.get('annotate', True):
        flags |= ANNOTATE
    
    return flags