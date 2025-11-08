import cv2
import numpy as np

img = cv2.imread(r"D:\dev\python\vscode_test\test_2\2-4.jpg",0)

down = cv2.pyrDown(img)
up = cv2.pyrUp(down)

# 调整up的尺寸与原始图像一致
up_resized = cv2.resize(up, (img.shape[1], img.shape[0]))

diff_img = img - up_resized  # 现在尺寸匹配了

# 添加归一化操作：将差异图像像素值归一化到0-255范围
min_val = np.min(diff_img)
max_val = np.max(diff_img)
# 处理max_val == min_val的特殊情况，避免除零错误
if max_val == min_val:
    normalized_img = np.zeros_like(diff_img, dtype=np.uint8)
else:
    normalized_img = ((diff_img - min_val) / (max_val - min_val) * 255).astype(np.uint8)

cv2.imshow('original_diff', diff_img)
cv2.imshow('normalized_diff', normalized_img)



#v1=cv2.Canny(img,80,150)
#v2=cv2.Canny(img,50,100)
#res = np.hstack((v1,v2))
#res=cv2.pyrUp(res)

#cv2.imshow('res',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
