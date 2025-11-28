from PIL import Image
import os
import os
import shutil

def lossless_crop_png(input_path: str, output_path: str, left: int, top: int, right: int, bottom: int):
    """
    对 PNG 图片进行无损裁剪
    :param input_path: 输入 PNG 文件路径
    :param output_path: 输出 PNG 文件路径
    :param left: 裁剪框左上角 x 坐标
    :param top: 裁剪框左上角 y 坐标
    :param right: 裁剪框右下角 x 坐标（不含）
    :param bottom: 裁剪框右下角 y 坐标（不含）
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    with Image.open(input_path) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        cropped = img.crop((left, top, right, bottom))

        # 保留 PNG 的透明通道，确保无损
        cropped.save(output_path, 'PNG', optimize=True)

if __name__ == "__main__":
    # 示例用法
    input_dir = "七年级英语课本"
    output_dir = "七年级英语课本_cut"

    # 如果输出目录不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录下所有png文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            # 逐一进行裁剪并保存到输出目录
            lossless_crop_png(input_path, output_path, 402, 122, 2152, 1351)
    # lossless_crop_png("ebook_screenshots/ebook_20251128_114554.png", "output.png", 402, 122, 2152, 1351)
