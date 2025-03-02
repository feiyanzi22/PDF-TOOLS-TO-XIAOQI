from tools.pdf_merge import pdf_merge
from tools.pdf_split import pdf_split
from tools.pdf_encrypt import pdf_encrypt
from tools.pdf_decrypt import pdf_decrypt
from tools.pdf_watermark import pdf_watermark
from tools.pdf_to_word import pdf_to_word
from tools.pdf_to_md import pdf_to_md
from tools.pdf_to_image import pdf_to_image
from tools.image_to_pdf import image_to_pdf
from tools.pdf_remove_watermark import pdf_remove_watermark

def main():
    while True:
        print("欢迎使用工具箱！")
        print("1. PDF 合并（支持文件夹和自定义顺序）")
        print("2. PDF 拆分")
        print("3. PDF 加密")
        print("4. PDF 解密")
        print("5. PDF 加水印")
        print("6. PDF 去水印")
        print("7. PDF 转 Word")
        print("8. PDF 转 Markdown")
        print("9. PDF 转图片")
        print("10. 图片转 PDF")
        print("11. 退出")
        
        choice = input("请输入选项（1-11）：")
        
        if choice == "1":
            pdf_merge()
        elif choice == "2":
            pdf_split()
        elif choice == "3":
            pdf_encrypt()
        elif choice == "4":
            pdf_decrypt()
        elif choice == "5":
            pdf_watermark()
        elif choice == "6":
            pdf_remove_watermark()
        elif choice == "7":
            pdf_to_word()
        elif choice == "8":
            pdf_to_md()
        elif choice == "9":
            pdf_to_image()
        elif choice == "10":
            image_to_pdf()
        elif choice == "11":
            print("退出程序")
            break
        else:
            print("无效选项，请重试")
            continue

if __name__ == "__main__":
    main()