import cv2

def callback():
    pass

cv2.namedWindow('color',cv2.WINDOW_GUI_NORMAL)

img=cv2.imread('two_test/2-4.jpg')
import cv2

def callback():
    pass

# 1. 创建窗口（保持不变）
cv2.namedWindow('color', cv2.WINDOW_GUI_NORMAL)

# 2. 修正路径：用正斜杠或双反斜杠，同时增加读取判断
img = cv2.imread('two_test/2-4.jpg')  # 修正路径（方案1：正斜杠）
# img = cv2.imread('two_test\\2-4.jpg')  # 修正路径（方案2：双反斜杠，二选一即可）

if img is None:  # 容错：判断图像是否成功读取
    print("错误：无法读取图像文件！请检查：")
    print("1. 路径是否正确（当前路径：two_test/2-4.jpg）")
    print("2. 图像文件是否存在、格式是否支持（如jpg/png）")
    exit()  # 读取失败则退出，避免后续报错

# 3. 颜色空间列表（上一版已修正COLOR_BGR2BGRA，此处保持正确）
colorspaces = [
    cv2.COLOR_BGR2RGBA,
    cv2.COLOR_BGR2BGRA,
    cv2.COLOR_BGR2GRAY,
    cv2.COLOR_BGR2HSV_FULL,
    cv2.COLOR_BGR2YUV
]

# 4. 修正滑动条最大值：避免索引越界
cv2.createTrackbar('curcolor', 'color', 0, len(colorspaces)-1, callback)

while True:
    # 获取当前滑动条索引
    index = cv2.getTrackbarPos('curcolor', 'color')
    
    # 转换颜色空间（逻辑正确，保持不变）
    cvt_img = cv2.cvtColor(img, colorspaces[index])
    
    # 5. 修正显示：显示转换后的图像
    cv2.imshow('color', cvt_img)
    
    # 等待按键（按'q'退出，保持不变）
    key = cv2.waitKey(10)
    if key & 0xFF == ord('q'):
        break

# 释放窗口资源（保持不变）
cv2.destroyAllWindows()

colorspaces=[cv2.COLOR_BGR2RGBA,cv2.COLOR_BGR2BGRA,
             cv2.COLOR_BGR2GRAY,cv2.COLOR_BGR2HSV_FULL,
             cv2.COLOR_BGR2YUV]

cv2.createTrackbar('curcolor','color',0,len(colorspaces),callback)

while True:
    index=cv2.getTrackbarPos('curcolor','color')


    cvt_img=cv2.cvtColor(img,colorspaces[index])
    cv2.imshow('color',img)
    key=cv2.waitKey(10)
    if key & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()