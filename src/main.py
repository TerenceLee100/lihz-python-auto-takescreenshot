import pyautogui
import time
import keyboard
import os
import random
from datetime import datetime
from get_mouse_position import get_mouse_position   

# ===================== 配置参数（根据实际情况修改）=====================
CLICK_X = 2473  # 翻页按钮X坐标（替换为你获取的坐标）
CLICK_Y = 1381   # 翻页按钮Y坐标（替换为你获取的坐标）
CLICK_RANGE = 10  # 点击坐标范围（±10像素，适配按钮轻微偏移）
SLEEP_AFTER_CLICK = 5  # 点击后等待截屏的时间（秒）
SCREENSHOT_SAVE_PATH = "./ebook_screenshots"  # 截屏保存路径
STOP_KEY = "esc"  # 停止脚本的按键（ESC键，可改为其他如"ctrl+q"）
# =====================================================================

# 创建截屏保存目录（不存在则自动创建）
if not os.path.exists(SCREENSHOT_SAVE_PATH):
    os.makedirs(SCREENSHOT_SAVE_PATH)

def random_click_in_range(x, y, range_pixel):
    """在指定坐标范围内随机点击（避免固定坐标被反爬/按钮偏移）"""
    click_x = random.randint(x - range_pixel, x + range_pixel)
    click_y = random.randint(y - range_pixel, y + range_pixel)
    pyautogui.click(click_x, click_y, duration=0.2)  # duration=0.2模拟人类点击速度
    print(f"已点击翻页按钮，坐标：({click_x}, {click_y})")

def take_screenshot():
    """截取全屏并保存（命名格式：时间戳.jpg，避免覆盖）"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(SCREENSHOT_SAVE_PATH, f"ebook_{timestamp}.png")
    pyautogui.screenshot(screenshot_path)
    print(f"已截屏保存：{screenshot_path}")

def main():
    print("===== 电子书自动翻页+截屏脚本 =====")
    print(f"停止脚本请按：{STOP_KEY}键")
    print("脚本即将启动...（3秒后开始）")
    time.sleep(3)

    try:
        while True:
            # 1. 检查是否按下停止键
            if keyboard.is_pressed(STOP_KEY):
                print(f"\n检测到{STOP_KEY}键，脚本停止运行")
                break

            # 2. 点击翻页按钮
            random_click_in_range(CLICK_X, CLICK_Y, CLICK_RANGE)

            # 3. 等待5秒（让页面加载完成）
            time.sleep(SLEEP_AFTER_CLICK)

            # 4. 截屏
            take_screenshot()

            # 可选：翻页后短暂等待（避免操作过快）
            time.sleep(0.5)

    except Exception as e:
        print(f"脚本异常停止：{e}")
    finally:
        print("脚本已退出")

if __name__ == "__main__":
    # CLICK_X, CLICK_Y = get_mouse_position()
    main()