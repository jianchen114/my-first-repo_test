import cv2
import time
import numpy as np
# 打开摄像头
capture = cv2.VideoCapture(0)
# 检查摄像头是否成功打开
if not capture.isOpened():
    print("无法打开摄像头")
    exit()
# 获取摄像头的宽高和帧率信息
frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = capture.get(cv2.CAP_PROP_FPS)
# 如果无法获取摄像头帧率，使用默认值30
if fps <= 0:
    fps = 30
# 定义编码器和创建VideoWriter对象
# 使用MP4V编码器，输出MP4格式文件
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))
# 用于平滑FPS显示的参数
fps_buffer = []
buffer_size = 10  # 滑动窗口大小
prev_time = time.time()
while True:
    ret, frame = capture.read()
    if not ret:
        print("无法接收帧（流已结束？）。退出...")
        break  # 如果读取失败则退出循环
    
    # 计算并显示FPS（滑动平均优化）

    #frame_time = current_time - prev_time
    #prev_time = current_time
    
    #if frame_time > 0:
    #    current_fps = 1 / frame_time
    #    if len(fps_buffer) > buffer_size:
    #        fps_buffer.pop(0)
    #    display_fps = np.mean(fps_buffer)
        
    #    cv2.putText(frame, f"FPS: {display_fps:.2f}", (10, 30), 
    #                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 将帧写入输出文件
    out.write(frame)
    # 显示摄像头画面
    cv2.imshow("camera", frame)
    
    # 按'q'键或关闭窗口退出
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    # 检查窗口是否被关闭
    if cv2.getWindowProperty("camera", cv2.WND_PROP_VISIBLE) < 1:
        break
# 释放资源
capture.release()
out.release()  # 释放视频写入器
cv2.destroyAllWindows()
