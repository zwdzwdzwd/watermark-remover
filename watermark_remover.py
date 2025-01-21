import cv2
import numpy as np

def remove_watermark(input_path, output_path):
    # 读取图像
    img = cv2.imread(input_path)
    
    # 转换到灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 增强对比度
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # 二值化处理，使用 Otsu 算法自动确定阈值
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 降噪处理
    denoised = cv2.fastNlMeansDenoising(binary)
    
    # 形态学操作，去除细小噪点
    kernel = np.ones((2,2), np.uint8)
    cleaned = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
    
    # 锐化处理
    kernel_sharpen = np.array([[-1,-1,-1],
                              [-1, 9,-1],
                              [-1,-1,-1]])
    sharpened = cv2.filter2D(cleaned, -1, kernel_sharpen)
    
    # 保存结果
    cv2.imwrite(output_path, sharpened)

def main():
    input_path = "input.jpg"  # 替换为您的输入图像路径
    output_path = "output.jpg"  # 输出图像路径
    
    try:
        remove_watermark(input_path, output_path)
        print("水印去除完成！输出文件已保存为:", output_path)
    except Exception as e:
        print("处理过程中出现错误:", str(e))

if __name__ == "__main__":
    main()