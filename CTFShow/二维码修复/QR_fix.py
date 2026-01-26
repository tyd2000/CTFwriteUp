import numpy as np
from PIL import Image, ImageDraw
import cv2

def detect_qr_structure(image_path):
    """检测QR码结构"""
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    # 转换为灰度图
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    # 使用自适应阈值
    binary = cv2.adaptiveThreshold(gray, 255, 
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)
    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 找到最大的轮廓（假设是QR码）
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        # 确保有合理的边界
        x = max(0, x-5)
        y = max(0, y-5)
        w = min(width-x, w+10)
        h = min(height-y, h+10)
        # 裁剪QR码区域
        qr_region = img_array[y:y+h, x:x+w]
        return qr_region, (x, y, w, h)
    return img_array, (0, 0, width, height)

def estimate_module_size(qr_region):
    """估计模块大小"""
    height, width = qr_region.shape[:2]
    # 转换为灰度
    gray = cv2.cvtColor(qr_region, cv2.COLOR_RGB2GRAY)
    # 取中间几行进行采样
    sample_row = gray[height//2, :]
    # 计算黑白转换
    is_black = sample_row < 128
    changes = np.where(is_black[:-1] != is_black[1:])[0]
    if len(changes) > 5:
        # 计算相邻变化之间的距离
        distances = np.diff(changes)
        # 去除异常值（太大或太小的距离）
        median_dist = np.median(distances)
        distances = distances[(distances > median_dist*0.5) & (distances < median_dist*2)]
        module_size = np.median(distances) if len(distances) > 0 else max(1, width // 40)
    else:
        module_size = max(1, width // 40)
    return int(round(module_size))

def create_finder_pattern(module_size):
    """创建定位块图案"""
    # 确保模块大小至少为1
    module_size = max(1, module_size)
    size = 7 * module_size
    # 创建图案
    pattern = np.ones((size, size, 3), dtype=np.uint8) * 255  # 白色背景
    # 绘制黑色边框
    pattern[:module_size, :] = [0, 0, 0]  # 上边框
    pattern[-module_size:, :] = [0, 0, 0]  # 下边框
    pattern[:, :module_size] = [0, 0, 0]  # 左边框
    pattern[:, -module_size:] = [0, 0, 0]  # 右边框
    # 绘制白色边框内的区域
    pattern[module_size:-module_size, module_size:-module_size] = [255, 255, 255]
    # 绘制中心黑色方块 (3x3)
    center_start = 2 * module_size
    center_end = 5 * module_size
    pattern[center_start:center_end, center_start:center_end] = [0, 0, 0]
    # 绘制中心白色点
    white_start = 3 * module_size
    white_end = 4 * module_size
    pattern[white_start:white_end, white_start:white_end] = [255, 255, 255]
    return pattern

def find_qr_corners(qr_region, module_size):
    """查找QR码的角点"""
    height, width = qr_region.shape[:2]
    # 假设标准QR码结构
    # 尝试不同版本 (1-40)
    for version in range(1, 41):
        total_modules = 17 + 4 * version
        estimated_width = total_modules * module_size
        # 如果估计的宽度接近实际宽度，则采用此版本
        if abs(estimated_width - width) <= module_size * 2:
            # 计算角点位置
            finder_size = 7 * module_size
            corners = {
                'top_left': (0, 0),
                'top_right': (0, width - finder_size),
                'bottom_left': (height - finder_size, 0)
            }
            return corners, version
    # 如果无法确定版本，使用默认位置
    finder_size = 7 * module_size
    corners = {
        'top_left': (0, 0),
        'top_right': (0, width - finder_size),
        'bottom_left': (height - finder_size, 0)
    }
    return corners, 1

def repair_qr_code_robust(image_path, output_path='repaired_qr.png'):
    """健壮的QR码修复函数"""
    try:
        # 1. 检测并裁剪QR码区域
        qr_region, bbox = detect_qr_structure(image_path)
        print(f"QR码区域: 位置={bbox[0:2]}, 尺寸={bbox[2:4]}")
        # 2. 估计模块大小
        module_size = estimate_module_size(qr_region)
        print(f"估计模块大小: {module_size} 像素")
        # 确保模块大小合理
        if module_size <= 0:
            module_size = max(1, bbox[2] // 40)
            print(f"调整模块大小为: {module_size} 像素")
        # 3. 创建定位块图案
        finder_pattern = create_finder_pattern(module_size)
        pattern_size = finder_pattern.shape[0]
        print(f"定位块尺寸: {pattern_size}x{pattern_size} 像素")
        # 4. 查找角点位置
        corners, version = find_qr_corners(qr_region, module_size)
        print(f"估计QR码版本: {version}")
        print(f"角点位置: {corners}")
        # 5. 复制原始图像
        repaired = qr_region.copy()
        # 6. 在三个角点绘制定位块
        for corner_name, (y, x) in corners.items():
            # 确保坐标有效
            if x >= 0 and y >= 0 and x + pattern_size <= repaired.shape[1] and y + pattern_size <= repaired.shape[0]:
                repaired[y:y+pattern_size, x:x+pattern_size] = finder_pattern
                print(f"在 {corner_name} ({y}, {x}) 绘制定位块")
            else:
                print(f"警告: {corner_name} 位置无效，跳过")
        # 7. 保存修复后的图像
        repaired_img = Image.fromarray(repaired)
        repaired_img.save(output_path)
        print(f"修复完成，图像已保存到: {output_path}")
        # 8. 显示修复后的图像
        repaired_img.show()
        return repaired_img
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        print("尝试备用方法...")
        return repair_qr_code_simple(image_path, output_path)

def repair_qr_code_simple(image_path, output_path='repaired_qr_simple.png'):
    """简单的QR码修复方法"""
    try:
        # 直接加载图像
        img = Image.open(image_path).convert('RGB')
        width, height = img.size
        # 估计模块大小
        module_size = max(1, min(width, height) // 40)
        # 创建定位块
        finder_pattern = create_finder_pattern(module_size)
        pattern_size = finder_pattern.shape[0]
        # 转换为numpy数组
        img_array = np.array(img)
        # 在三个角点绘制定位块
        positions = [
            (0, 0),  # 左上
            (0, width - pattern_size),  # 右上
            (height - pattern_size, 0)  # 左下
        ]
        for y, x in positions:
            if x >= 0 and y >= 0 and x + pattern_size <= width and y + pattern_size <= height:
                img_array[y:y+pattern_size, x:x+pattern_size] = finder_pattern
        # 保存图像
        repaired_img = Image.fromarray(img_array)
        repaired_img.save(output_path)
        print(f"简单修复完成，图像已保存到: {output_path}")        
        return repaired_img
    except Exception as e:
        print(f"简单修复也失败: {e}")
        return None

def decode_repaired_qr(image_path):
    """尝试解码修复后的QR码"""
    try:
        # 尝试使用pyzbar
        from pyzbar.pyzbar import decode 
        img = Image.open(image_path)
        decoded = decode(img) 
        if decoded:
            print("解码成功!")
            for d in decoded:
                print(f"  类型: {d.type}")
                print(f"  内容: {d.data.decode('utf-8')}")
            return True
        else:
            print("解码失败")
            return False 
    except ImportError:
        print("未安装pyzbar，无法自动解码")
        print("请手动扫描图像或安装pyzbar: pip install pyzbar")
        return False
    except Exception as e:
        print(f"解码错误: {e}")
        return False

def decode_qr(image_path: str)->str:
    """ 从指定路径中读取扫描二维码图片解码出QR内容 """
    try:
        img = Image.open(image_path)
    except Exception as e:
        raise ValueError(f"无法打开图像文件 '{image_path}': {e}")
    from pyzbar import pyzbar
    barcodes = pyzbar.decode(img)
    data = ''.join(barcode.data.decode('utf-8') for barcode in barcodes)
    return data


# 主程序
if __name__ == "__main__":
    import sys
    import os
    # 检查命令行参数
    if len(sys.argv) > 1:
        input_image = sys.argv[1]
    else:
        input_image = input("请输入损坏的QR码图像路径: ")
    if not os.path.exists(input_image):
        print(f"错误: 文件 '{input_image}' 不存在")
        sys.exit(1)
    # 修复QR码
    print("=" * 50)
    print("开始修复QR码...")
    print("=" * 50)
    # 健壮修复
    output_file = "repaired_qr.png"
    repaired = repair_qr_code_robust(input_image, output_file)
    """
    if repaired:
        # 尝试解码
        print("\n尝试解码修复后的QR码...")
        decode_repaired_qr("repaired_qr.png")
        # 如果失败，尝试简单方法
        if not os.path.exists("repaired_qr.png") or not decode_repaired_qr("repaired_qr.png"):
            print("\n健壮修复失败，尝试简单修复...")
            repaired_simple = repair_qr_code_simple(input_image, "repaired_qr_simple.png")
            if repaired_simple:
                print("\n尝试解码简单修复后的QR码...")
                decode_repaired_qr("repaired_qr_simple.png")
    """
    print("\n修复完成！请查看生成的图像文件。")
    try:
        msg = decode_qr(output_file)
        if msg:
            print("解码成功:", msg)
        else:
            print("未检测到有效二维码")
    except Exception as e:
        print("解码失败:", e)
    # ctfshow单身杯misc签到题
    flag = bytes.fromhex(msg).decode()
    # lue, far exceeds your belief}
    flag = 'ctfshow{Your potential,va'+flag
    print(flag)
    # ctfshow{Your potential,value, far exceeds your belief}
    flag = flag.replace(" ", "_").replace(",", "_")
    print(f'🎉Final Flag is found!\n{flag}')
    # ctfshow{Your_potential_value__far_exceeds_your_belief}