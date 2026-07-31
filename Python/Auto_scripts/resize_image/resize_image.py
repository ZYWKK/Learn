from pathlib import Path

from PIL import Image  # 从 PIL 库（Pillow）中导入 Image 模块，用于处理图像

# 调整图像尺寸的函数
def resize_image(input_path, output_path, width, height, overwrite=False):
    """
    将输入的图像调整为指定宽度和高度，并保存到输出路径。

    参数:
    input_path (str): 输入图像的文件路径。
    output_path (str): 调整后图像的保存路径。
    width (int): 调整后图像的宽度（像素）。
    height (int): 调整后图像的高度（像素）。
    """
    if Path(output_path).exists() and not overwrite:
        raise FileExistsError(f"输出文件已存在: {output_path}")

    # 使用上下文管理器确保图像文件及时关闭。
    with Image.open(input_path) as image:
        # 使用 Pillow 当前推荐的 Lanczos 重采样算法提高缩放质量
        resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
        resized_image.save(output_path)

# 使用示例
if __name__ == "__main__":
    # 调用 resize_image 函数，将输入图像调整为800x600像素
    resize_image('/path/to/input.jpg', '/path/to/output.jpg', 800, 600)  # 请将路径替换为实际的输入和输出图像路径
