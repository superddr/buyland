
import keyboard, threading

def buy_land():
    """这里放你已经写好的购买逻辑"""
    print("Ctrl+L 被按下，开始自动购买地块...")
    
    import mss, numpy as np, cv2
    with mss.mss() as sct:
        frame = np.array(sct.grab(sct.monitors[0]))  # BGRA
    cv2.imwrite("a.jpg",frame)

# 注册全局热键（异步回调，不阻塞主线程）
keyboard.add_hotkey('ctrl+c', buy_land)

# 保持脚本常驻
keyboard.wait('ctrl+/')   # 按 Esc 退出监听
