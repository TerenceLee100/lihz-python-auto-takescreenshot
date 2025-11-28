import pyautogui
import time
import keyboard

def get_mouse_position():
    """
    显示鼠标当前位置的实时坐标
    按ESC键退出程序
    """
    print("===== 鼠标坐标获取工具 =====")
    print("将鼠标移动到需要获取坐标的位置(最好是需要点击的区域的中心位置，后续脚本将在这个中心区域附近进行点击活动，避免被反爬机制屏蔽掉)，屏幕上会显示当前坐标")
    print("按 ESC 键退出程序")
    print("\n当前鼠标坐标：")
    
    try:
        while True:
            # 获取鼠标当前位置
            x, y = pyautogui.position()
            
            # 在同一行显示坐标，每秒更新
            print(f"\rX: {x:4d}, Y: {y:4d}", end="", flush=True)
            
            # 检查是否按下ESC键
            if keyboard.is_pressed('esc'):
                return x, y
                break
            
            # 每秒更新一次
            time.sleep(1)
    
    except KeyboardInterrupt:
        pass
    finally:
        print("\n\n程序已退出")

if __name__ == "__main__":
    get_mouse_position()
