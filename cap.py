
import keyboard, threading

from det import GameElementDetector
det = GameElementDetector(tpl_dir='tpl', threshold=0.75)

import win32api, win32con, time

def click(x: int, y: int, wait=0.05):
    win32api.SetCursorPos((x, y))
    time.sleep(wait)  
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def buy_land():
    while(True):
        click(1001,915,0.2)
        print("点购买")
        cv2.waitKey(200)

        import mss, numpy as np,cv2
        with mss.mss() as sct:
            frame = np.array(sct.grab(sct.monitors[0]))  # BGRA

        img = frame[:,:,:3]
        boxes = det.detect(img)
        print("找到",len(boxes),"个目标")
        if len(boxes)==0:
            print("买完")
            break
        
        box = boxes[0]
        x=int((box["x1"]+box["x2"])/2)
        y=int((box["y1"]+box["y2"])/2)
        click(x,y)
        print("点金币")
        
        
        
# 注册全局热键（异步回调，不阻塞主线程）
keyboard.add_hotkey('ctrl+.', buy_land)
print("等待Ctrl+. 被按下，开始自动购买地块...")
# 保持脚本常驻
keyboard.wait('ctrl+l')   # 按 Esc 退出监听
