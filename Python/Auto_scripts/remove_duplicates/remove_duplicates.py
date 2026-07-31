import os

import pandas as pd  # 导入 pandas 库，用于处理数据

# 从Excel文件中移除重复行的函数
def remove_duplicates(file_path, output_path=None):
    """
    从指定Excel文件中移除重复行，并默认保存为新文件。

    参数:
    file_path (str): Excel文件的路径。
    output_path (str): 可选输出路径；省略时生成 *_deduplicated 文件。
    """
    # 使用 pandas 读取 Excel 文件，存储为 DataFrame
    df = pd.read_excel(file_path)

    # 使用 drop_duplicates() 方法移除重复的行
    df.drop_duplicates(inplace=True)

    if output_path is None:
        stem, extension = os.path.splitext(file_path)
        output_path = f"{stem}_deduplicated{extension}"

    # 默认保存为新文件；只有显式传入相同路径时才会覆盖原文件。
    df.to_excel(output_path, index=False)
    return output_path

# 使用示例
if __name__ == "__main__":
    # 默认生成 data_deduplicated.xlsx，保留原文件。
    result_path = remove_duplicates('/path/to/data.xlsx')
    print(f"去重结果已保存到: {result_path}")
