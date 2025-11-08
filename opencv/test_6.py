import cv2
import numpy as np

def detect_shapes(image_path):
    """
    检测图像中的特定形状（长方形、正方形、三角形）并标记出来
    
    参数:
        image_path (str): 图像文件的路径
    """
    # 读取图像文件
    img = cv2.imread(image_path)
    # 检查图像是否读取成功
    if img is None:
        print("图片读取失败！")
        return

    # 将BGR色彩空间转换为HSV色彩空间，便于颜色过滤
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 创建图像副本用于绘制检测结果，避免修改原图
    result = img.copy()

    # 定义各形状的颜色范围和形状判断逻辑
    # 每个形状包含：名称、HSV颜色范围、形状判断函数
    shapes = [
        {
            "name": "recangle",
            # 绿色的HSV范围（低阈值，高阈值）
            "color_range": (np.array([35, 50, 50]), np.array([77, 255, 255])),
            # 判断逻辑：4个顶点且宽高比不在正方形范围内（0.95-1.05）
            "shape_check": lambda approx: len(approx) == 4 and not (0.95 <= (cv2.boundingRect(approx)[2]/cv2.boundingRect(approx)[3]) <= 1.05)
        },
        {
            "name": "square",
            # 橙色的HSV范围（低阈值，高阈值）
            "color_range": (np.array([10, 50, 50]), np.array([25, 255, 255])),
            # 判断逻辑：4个顶点且宽高比在0.95-1.05范围内（近似正方形）
            "shape_check": lambda approx: len(approx) == 4 and 0.95 <= (cv2.boundingRect(approx)[2]/cv2.boundingRect(approx)[3]) <= 1.05
        },
        {
            "name": "triangle",
            # 黄色的HSV范围（低阈值，高阈值）
            "color_range": (np.array([20, 50, 50]), np.array([30, 255, 255])),
            # 判断逻辑：3个顶点
            "shape_check": lambda approx: len(approx) == 3
        }
    ]

    # 遍历每种形状的检测参数
    for shape in shapes:
        # 获取当前形状的颜色范围
        lower, upper = shape["color_range"]
        # 根据颜色范围创建掩码（只保留在范围内的颜色）
        mask = cv2.inRange(hsv, lower, upper)
        
        # 形态学操作优化掩码
        # 创建5x5的结构元素
        kernel = np.ones((5, 5), np.uint8)
        # 先进行闭操作：填充小的空洞，连接断开的区域
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # 再进行开操作：去除小的噪点，平滑边界
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # 从优化后的掩码中寻找轮廓
        # RETR_EXTERNAL：只检测最外层轮廓
        # CHAIN_APPROX_SIMPLE：压缩水平、垂直和对角线方向的轮廓点，只保留端点
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 遍历每个找到的轮廓

        col=[(0, 255, 0), (0, 0, 255), (255, 0, 0),
    (0, 255, 255), (255, 255, 0), (255, 0, 255)]
        i=0

        for cnt in contours:
            # 计算轮廓面积，过滤面积过小的轮廓（排除噪点）
            area = cv2.contourArea(cnt)
            if area < 100:
                continue
            
            # 计算轮廓周长（第二个参数True表示轮廓是闭合的）
            perimeter = cv2.arcLength(cnt, True)
            # 多边形逼近：将轮廓近似为更简单的多边形
            # 0.03*perimeter：逼近精度，值越小越接近原始轮廓
            approx = cv2.approxPolyDP(cnt, 0.03 * perimeter, True)
            
            # 检查当前轮廓是否符合当前形状的判断条件
            if shape["shape_check"](approx):
                # 在结果图像上绘制轮廓（绿色，线宽2）
                cv2.drawContours(result, [approx], -1, col[i], 2)
                # 获取轮廓的边界矩形
                x, y, w, h = cv2.boundingRect(approx)
                # 确定标签位置：避免标签超出图像范围
                label_pos = (x, y-10) if y > 10 else (x, y+h+20)
                # 在图像上绘制形状名称（绿色，字体大小0.7，线宽2）
                cv2.putText(result, shape["name"], label_pos,
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, col[i], 2)
            
            i+=2

    cv2.imshow("Shape Detection", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = r"test_2\2-6.png"  
    detect_shapes(image_path)