from PIL import Image
import os
import os
import shutil

def split_image_left_right(image_path, output_dir):
    """
    Split an image into left and right halves and save them.
    
    Args:
        image_path: Path to the input image
        output_dir: Directory to save the split images
    """
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    
    # Calculate middle point
    middle = width // 2
    
    # Split into left and right
    left_img = img.crop((0, 0, middle, height))
    right_img = img.crop((middle, 0, width, height))
    
    # Prepare output paths
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    left_path = os.path.join(output_dir, f"{base_name}_left.png")
    right_path = os.path.join(output_dir, f"{base_name}_right.png")
     
    # Save the images
    left_img.save(left_path)
    right_img.save(right_path)
    
    return left_path, right_path

# Example usage:
# 

if __name__ == "__main__":
    # 示例用法
    input_dir = "ebook_screenshots"
    output_dir = "ebook_screenshots_cut"

    # 如果输出目录不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录下所有png文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            # output_path = os.path.join(output_dir, filename)
            # 逐一进行裁剪并保存到输出目录
            split_image_left_right(input_path, output_dir)