import cv2
import numpy as np

def preprocess_image(image):
    """预处理图像，针对低边缘特征图像优化"""
    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 轻度高斯模糊保留更多细节
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    # 自适应阈值处理增强区域对比度
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY_INV, 11, 2)
    
    # 形态学操作优化区域连接
    kernel = np.ones((2, 2), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return opened

def detect_shapes(image_path):
    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        print("图片读取失败！")
        return
    
    # 创建原图副本用于绘制
    result = img.copy()
    
    # 预处理图像
    processed = preprocess_image(img)
    
    # 转换为HSV色彩空间，增加容差范围
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 扩展颜色范围容差，适应不同光照下的彩色填充区域
    color_ranges = {
        'red': (np.array([0, 80, 50]), np.array([10, 255, 255])),
        'red2': (np.array([170, 80, 50]), np.array([180, 255, 255])),  # 红色的另一范围
        'green': (np.array([30, 60, 60]), np.array([80, 255, 255])),
        'blue': (np.array([90, 60, 60]), np.array([130, 255, 255])),
        'yellow': (np.array([15, 60, 60]), np.array([35, 255, 255]))
    }
    
    # 形状检测配置
    shape_configs = {
        'square': {
            'check': is_square,
            'color': (0, 255, 0)  # 绿色框
        },
        'rectangle': {
            'check': is_rectangle,
            'color': (255, 0, 0)  # 蓝色框
        },
        'triangle': {
            'check': is_triangle,
            'color': (0, 0, 255)  # 红色框
        }
    }
    
    # 初始化计数器
    shape_count = {shape: 0 for shape in shape_configs}
    
    # 对每种颜色进行检测
    for color_name, (lower, upper) in color_ranges.items():
        # 处理红色的特殊情况（两个范围）
        if color_name == 'red2':
            actual_name = 'red'
        else:
            actual_name = color_name
        
        # 创建颜色掩码
        color_mask = cv2.inRange(hsv, lower, upper)
        
        # 增强颜色掩码的连通性
        kernel = np.ones((3, 3), np.uint8)
        color_mask = cv2.dilate(color_mask, kernel, iterations=1)
        color_mask = cv2.erode(color_mask, kernel, iterations=1)
        
        # 结合处理后的掩码和颜色掩码
        combined_mask = cv2.bitwise_and(color_mask, processed)
        
        # 查找轮廓（保留内部轮廓，适应填充区域）
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            # 过滤小面积轮廓
            area = cv2.contourArea(cnt)
            if area < 50:  # 减小面积阈值，适应小形状
                continue
            
            # 轮廓近似（降低精度要求，适应边缘不明显的情况）
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            # 调整近似系数，值越大轮廓越简单
            approx = cv2.approxPolyDP(cnt, 0.05 * perimeter, True)
            
            # 检查每种形状
            for shape_name, config in shape_configs.items():
                if config['check'](approx):
                    # 绘制轮廓
                    cv2.drawContours(result, [approx], -1, config['color'], 2)
                    # 绘制标签
                    x, y = approx[0][0]
                    cv2.putText(result, f"{actual_name} {shape_name}", 
                               (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.5, config['color'], 2)
                    shape_count[shape_name] += 1
                    break  # 找到匹配的形状后跳出循环
    
    # 显示统计结果
    y_offset = 30
    for shape, count in shape_count.items():
        cv2.putText(result, f"{shape}: {count}", (10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        print(f"{shape}: {count} 个")
        y_offset += 30
    
    # 显示结果
    cv2.imshow('Original Image', img)
    cv2.imshow('Processed Mask', processed)
    cv2.imshow('Shape Detection Result', result)
    while True:
        if cv2.waitKey(0) & 0xFF == 27:  # 按ESC键退出
            break

        cv2.destroyAllWindows()
        
# 形状检测函数
def is_triangle(approx):
    return len(approx) == 3

def is_square(approx):
    if len(approx) != 4:
        return False
    x, y, w, h = cv2.boundingRect(approx)
    aspect_ratio = float(w) / h
    return 0.85 <= aspect_ratio <= 1.15  # 增加误差容忍度

def is_rectangle(approx):
    if len(approx) != 4:
        return False
    x, y, w, h = cv2.boundingRect(approx)
    aspect_ratio = float(w) / h
    # 非正方形的四边形视为长方形，增加误差容忍度
    return not (0.85 <= aspect_ratio <= 1.15)

if __name__ == "__main__":
    image_path = r"test_2\2-6.png"  # 替换为你的图片路径
    detect_shapes(image_path)