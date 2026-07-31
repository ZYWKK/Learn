def find_replace(file_path, search_text, replace_text, dry_run=True):
    """
    在指定文件中查找并替换文本。

    参数:
    file_path (str): 要操作的文件路径。
    search_text (str): 要查找的文本。
    replace_text (str): 要替换为的新文本。
    dry_run (bool): 为 True 时只显示匹配数量，不写入文件。
    """
    if not search_text:
        raise ValueError('search_text 不能为空')

    # 使用 'with' 语句打开文件，读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()  # 读取整个文件内容为字符串

    # 使用 replace() 方法将所有匹配的文本替换为新的文本
    modified_text = text.replace(search_text, replace_text)

    if dry_run:
        print(f"预演：将替换 {text.count(search_text)} 处；文件尚未修改。")
        return

    # 明确设置 dry_run=False 后才覆盖原文件。
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_text)

# 使用示例
if __name__ == "__main__":
    # 调用 find_replace 函数，传入文件路径、要查找的文本和替换的文本
    find_replace('/path/to/file.txt', 'old', 'new')  # 默认只预演，不修改文件
