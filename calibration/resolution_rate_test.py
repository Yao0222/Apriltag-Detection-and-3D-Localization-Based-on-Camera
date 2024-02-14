import cv2

# 创建视频捕捉对象，参数0表示系统默认摄像头
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
else:
    # 获取当前分辨率
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print(f"当前摄像头分辨率为: {int(width)}x{int(height)}")

# 释放摄像头
cap.release()

# 当前摄像头分辨率为: 1280x720