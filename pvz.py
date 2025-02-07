import time
import cv2
import numpy as np
import pyautogui
import win32gui
import win32con
from pathlib import Path

# 防止鼠标移动太快
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

def find_window():
    """查找PVZ窗口"""
    print("正在查找游戏窗口...")
    target_title = "植物大战僵尸杂交版"

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if target_title in title:
                ctx.append(hwnd)
                print(f"找到游戏窗口：{title}")

    hwnds = []
    win32gui.EnumWindows(winEnumHandler, hwnds)
    return hwnds[0] if hwnds else None

def load_templates():
    """加载模板图片"""
    templates = {}
    script_dir = Path(__file__).parent
    
    template_files = {
        "重选": "chongxuan.png",
        "摇滚": "yaogun.png"
    }
    
    for name, filename in template_files.items():
        template_path = script_dir / filename
        if template_path.exists():
            print(f"加载模板：{template_path}")
            template = cv2.imread(str(template_path))
            if template is not None:
                templates[name] = {
                    'image': template,
                    'size': template.shape[:2]
                }
                print(f"模板 {name} 尺寸: {template.shape}")
            else:
                print(f"无法加载模板：{template_path}")
        else:
            print(f"模板文件不存在：{template_path}")
    
    return templates

def match_template(screenshot, template_info, threshold=0.8):
    """使用模板匹配查找按钮"""
    template = template_info['image']
    template_size = template_info['size']
    
    img_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    
    if locations:
        matches = []
        for loc in locations:
            match_info = {
                'top_left': loc,
                'bottom_right': (loc[0] + template_size[1], loc[1] + template_size[0]),
                'center': (loc[0] + template_size[1]//2, loc[1] + template_size[0]//2),
                'confidence': result[loc[1], loc[0]]
            }
            matches.append(match_info)
        
        return matches
    
    return []

def click_with_verification(x, y, name, confidence):
    """执行点击并验证"""
    print(f"\n准备点击 {name}:")
    print(f"目标坐标: ({x}, {y})")
    print(f"匹配置信度: {confidence:.2f}")
    
    pyautogui.moveTo(x, y, duration=0.5)
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(0.2)
    
    return True

def find_and_click_button(hwnd, template_info, name):
    """查找并点击特定按钮"""
    # 获取窗口位置并截图
    rect = win32gui.GetWindowRect(hwnd)
    x, y, x2, y2 = rect
    window_width = x2 - x
    window_height = y2 - y
    
    # 截图并转换格式
    screenshot = pyautogui.screenshot(region=(x, y, window_width, window_height))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    print(f"\n正在匹配模板：{name}")
    matches = match_template(screenshot, template_info)
    
    if matches:
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        best_match = matches[0]
        
        click_x = x + best_match['center'][0]
        click_y = y + best_match['center'][1]
        
        return click_with_verification(click_x, click_y, name, best_match['confidence'])
    
    return False

def wait_with_countdown(seconds):
    """等待指定时间，显示倒计时"""
    print(f"\n等待{seconds}秒...")
    for i in range(seconds, 0, -1):
        if i % 10 == 0:  # 每10秒显示一次倒计时
            print(f"还剩 {i} 秒...")
        time.sleep(1)

def main():
    try:
        # 加载模板
        templates = load_templates()
        if not templates:
            print("未能加载任何模板图片！")
            return
            
        print("\n开始运行，按Ctrl+C停止程序")
        while True:
            try:
                # 查找窗口
                hwnd = find_window()
                if not hwnd:
                    print("未找到游戏窗口，5秒后重试...")
                    time.sleep(5)
                    continue

                # 激活窗口
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(1)

                # 点击重选按钮
                print("\n尝试点击重选按钮...")
                if not find_and_click_button(hwnd, templates["重选"], "重选"):
                    print("未找到重选按钮，5秒后重试...")
                    time.sleep(5)
                    continue
                
                # 等待一小段时间后点击摇滚按钮
                time.sleep(2)
                print("\n尝试点击摇滚按钮...")
                if not find_and_click_button(hwnd, templates["摇滚"], "摇滚"):
                    print("未找到摇滚按钮，5秒后重试...")
                    time.sleep(5)
                    continue
                
                # 完成一轮点击，等待1分30秒
                wait_with_countdown(90)

            except Exception as e:
                print(f"循环中发生错误：{str(e)}")
                print("等待5秒后重试...")
                time.sleep(5)

    except KeyboardInterrupt:
        print("\n检测到键盘中断，程序结束")
    except Exception as e:
        print(f"发生错误：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()