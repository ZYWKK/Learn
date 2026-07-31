from PyPDF2 import PdfReader  # 导入 PdfReader，用于处理 PDF 文件

# 从 PDF 文件中提取文本的函数
def extract_text_from_pdf(pdf_path):
    """
    从指定的 PDF 文件中提取文本。

    参数:
    pdf_path (str): PDF 文件的路径。

    返回:
    str: 提取出的文本内容。
    """
    reader = PdfReader(pdf_path)
    text = ''  # 用于存储提取的文本

    # 遍历 PDF 文件的每一页，提取文本
    for page in reader.pages:
        text += page.extract_text() or ''

    return text  # 返回所有提取的文本内容

# 使用示例
if __name__ == "__main__":
    # 调用 extract_text_from_pdf 函数，提取指定 PDF 文件的文本内容
    text = extract_text_from_pdf('/path/to/document.pdf')  # 请将 '/path/to/document.pdf' 替换为实际文件路径
    # 打印提取出的文本内容
    print(text)
