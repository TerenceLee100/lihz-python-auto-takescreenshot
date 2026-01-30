import pyautogui
import time
import keyboard
import os
import random
from datetime import datetime
from image_cut_tool import lossless_crop_png
from image_split_tool import split_image_left_right

# ===================== 配置参数（根据实际情况修改）=====================
CLICK_X = 2473  # 翻页按钮X坐标（替换为你获取的坐标）
CLICK_Y = 1381   # 翻页按钮Y坐标（替换为你获取的坐标）
CLICK_RANGE = 10  # 点击坐标范围（±10像素，适配按钮轻微偏移）
SLEEP_AFTER_CLICK = 5  # 点击后等待截屏的时间（秒）
SCREENSHOT_SAVE_PATH = "./ebook_screenshots"  # 截屏保存路径
STOP_KEY = "esc"  # 停止脚本的按键（ESC键，可改为其他如"ctrl+q"）
# =====================================================================

# 创建截屏保存目录（不存在则自动创建）


def random_click_in_range(x, y, range_pixel):
    """在指定坐标范围内随机点击（避免固定坐标被反爬/按钮偏移）"""
    click_x = random.randint(x - range_pixel, x + range_pixel)
    click_y = random.randint(y - range_pixel, y + range_pixel)
    pyautogui.click(click_x, click_y, duration=0.2)  # duration=0.2模拟人类点击速度
    print(f"已点击翻页按钮，坐标：({click_x}, {click_y})")

def take_screenshot(sub_dir):
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
    """截取全屏并保存（命名格式：时间戳.jpg，避免覆盖）"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(sub_dir, f"ebook_{timestamp}.png")
    pyautogui.screenshot(screenshot_path)
    print(f"已截屏保存：{screenshot_path}")

def main(max_click_count=1000,sub_dir="ebook_screenshots"):
    print("===== 电子书自动翻页+截屏脚本 =====")
    print(f"停止脚本请按：{STOP_KEY}键")
    print("脚本即将启动...（3秒后开始）")
    time.sleep(3)

    try:
        click_count = 0
        while True:
            # 1. 检查是否按下停止键
            if keyboard.is_pressed(STOP_KEY):
                print(f"\n检测到{STOP_KEY}键，脚本停止运行")
                break

            # 2. 点击翻页按钮
            random_click_in_range(CLICK_X, CLICK_Y, CLICK_RANGE)

            # 3. 等待5秒（让页面加载完成）
            time.sleep(SLEEP_AFTER_CLICK)

            click_count += 1
            if click_count >= max_click_count:
                print(f"已点击{click_count}次，脚本自动停止")
                break
            # 4. 截屏
            take_screenshot(sub_dir=sub_dir)

            # 可选：翻页后短暂等待（避免操作过快）
            time.sleep(0.5)

    except Exception as e:
        print(f"脚本异常停止：{e}")
    finally:
        print("脚本已退出")

if __name__ == "__main__":
    # CLICK_X, CLICK_Y = get_mouse_position()
    sub_dir = "九年级全一册"
    main(max_click_count=110,sub_dir=sub_dir)
    input_dir = f"{sub_dir}"
    output_dir = f"{sub_dir}_cut"

    # 先把边儿裁掉
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录下所有png文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            # 逐一进行裁剪并保存到输出目录
            lossless_crop_png(input_path, output_path, 402, 122, 2152, 1351)

    input_dir = f"{sub_dir}_cut"
    output_dir = f"{sub_dir}_cut_cut"

    # 从中间垂直切割成两张图片
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录下所有png文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            # output_path = os.path.join(output_dir, filename)
            # 逐一进行裁剪并保存到输出目录
            split_image_left_right(input_path, output_dir)