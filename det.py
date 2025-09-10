# detector.py
import cv2, numpy as np, itertools, pathlib, collections

class GameElementDetector:
    def __init__(self, tpl_dir='tpl', threshold=0.8, method=cv2.TM_CCOEFF_NORMED):
        self.threshold = threshold
        self.method = method
        self.templates = []
        for p in pathlib.Path(tpl_dir).glob('*.png'):
            tpl = cv2.imread(str(p))
            self.templates.append((p.stem, tpl))

    def _match_single(self, img, tpl, name):
        res = cv2.matchTemplate(img, tpl, self.method)
        if self.method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            loc = np.where(res <= 1-self.threshold)
            scores = 1 - res[loc]
        else:
            loc = np.where(res >= self.threshold)
            scores = res[loc]
        h, w = tpl.shape[:2]
        boxes = []
        for pt, score in zip(zip(*loc[::-1]), scores):
            x, y = pt
            boxes.append({'name': name, 'x1': x, 'y1': y,
                          'x2': x+w, 'y2': y+h, 'score': float(score)})
        return boxes

    @staticmethod
    def _nms(boxes, iou_thresh=0.3):
        # 简易 NMS
        if not boxes: return []
        boxes = sorted(boxes, key=lambda b: b['score'], reverse=True)
        keep = []
        while boxes:
            b = boxes.pop(0)
            keep.append(b)
            boxes = [x for x in boxes if
                     GameElementDetector._iou(b, x) < iou_thresh]
        return keep

    @staticmethod
    def _iou(a, b):
        ix1 = max(a['x1'], b['x1']); iy1 = max(a['y1'], b['y1'])
        ix2 = min(a['x2'], b['x2']); iy2 = min(a['y2'], b['y2'])
        inter = max(0, ix2-ix1) * max(0, iy2-iy1)
        ua = (a['x2']-a['x1'])*(a['y2']-a['y1']) + (b['x2']-b['x1'])*(b['y2']-b['y1']) - inter
        return inter / (ua + 1e-6)

    def detect(self, img_bgr):
        all_boxes = []
        for name, tpl in self.templates:
            all_boxes += self._match_single(img_bgr, tpl, name)
        return self._nms(all_boxes)

    def draw(self, img, boxes, thickness=2):
        color_map = collections.defaultdict(lambda: (0,255,0))
        for b in boxes:
            c = color_map[b['name']]
            cv2.rectangle(img, (b['x1'], b['y1']), (b['x2'], b['y2']), c, thickness)
            cv2.putText(img, f"{b['name']}:{b['score']:.2f}",
                        (b['x1'], b['y1']-5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, c, 1)
        return img
    


# live_detect.py
import cv2, mss, numpy as np
# from detector import GameElementDetector


def main():
    det = GameElementDetector(tpl_dir='tpl', threshold=0.75)
    # with mss.mss() as sct:
    #     monitor = sct.monitors[1]
    #     while True:
    # img = np.array(sct.grab(monitor))[:,:,:3][:,:,::-1]
    # img = cv2.imread("B.jpg")
    
    # vis = det.draw(img, boxes)
    # cv2.imshow('detect', vis)
    # cv2.waitKey(0) 
    
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()