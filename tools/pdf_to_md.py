import pdfplumber

def pdf_to_md():
    pdf_file = input("请输入 PDF 文件路径：")
    md_file = input("请输入输出的 Markdown 文件路径（比如 output.md）：")
    with pdfplumber.open(pdf_file) as pdf:
        with open(md_file, "w", encoding="utf-8") as md:
            for page in pdf.pages:
                text = page.extract_text()
                md.write(text + "\n\n")
    print("PDF 转 Markdown 完成！")