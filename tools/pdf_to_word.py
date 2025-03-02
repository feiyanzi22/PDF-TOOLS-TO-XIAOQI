from pdf2docx import Converter
import sys

def pdf_to_word():
    try:
        pdf_file = input("请输入 PDF 文件路径：")
        docx_file = input("请输入输出的 Word 文件路径（比如 output.docx）：")
        
        print("正在转换中，请稍候...")
        # 使用更简单的方法
        from pdf2docx.converter import parse
        parse(pdf_file, docx_file)
        print("PDF 转 Word 完成！")
    except Exception as e:
        print(f"发生错误: {e}")
        print("\n建议：")
        print("1. 确保PDF文件没有被加密")
        print("2. 如果PDF包含复杂图片，可以：")
        print("   - 先使用选项8将PDF转为图片")
        print("   - 然后使用其他OCR软件进行识别")