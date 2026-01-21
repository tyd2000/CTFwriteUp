import os
from PIL import Image
from collections import defaultdict

def NinePointSamplingAnalyze(image):
    """九点采样分析图像特征"""
    width, height = image.size
    imgObject = image.convert("RGB")
    pixels = imgObject.load()
    samplings = []
    for i in range(3):
        for j in range(3):
            samplePixel = pixels[(width - 1) if j == 2 else (width // 2) * j, 
                                 (height - 1) if i == 2 else (height // 2) * i]
            samplings.append(samplePixel)
    image.close()
    return samplings

def SamplingMatch(modelSample, sample):
    """计算两个采样特征的匹配度"""
    flag = 0
    for i in range(9):
        if sample[i] == modelSample["sample"][i]:
            flag += 1
    return flag

def SamplingBestRotate(modelSample, sample):
    """找到最佳旋转角度"""
    flags = []
    for i in range(4):
        flags.append(SamplingMatch(modelSample, sample))
        sample = SamplingRotate(sample)
    return max(flags), flags.index(max(flags)) * (-90)

def SamplingRotate(sample):
    """旋转采样特征（顺时针90度）"""
    newSamplings = []
    index = [6, 3, 0, 7, 4, 1, 8, 5, 2]
    for i in range(9):
        newSamplings.append(sample[index[i]])
    return newSamplings

def SamplingBestSolve(modelSamplings, sample):
    """从所有模型块中找到最佳匹配"""
    flags = []
    degrees = []
    for i in range(len(modelSamplings)):
        flag, degree = SamplingBestRotate(modelSamplings[i], sample)
        flags.append(flag)
        degrees.append(degree)
    return max(flags), flags.index(max(flags)), degrees[flags.index(max(flags))]

def split_image_by_block_size(image, block_width, block_height):
    """
    根据块大小分割图像
    """
    width, height = image.size
    cols = width // block_width
    rows = height // block_height
    
    # 确保整除，如果不是，调整图像大小
    if width % block_width != 0 or height % block_height != 0:
        new_width = cols * block_width
        new_height = rows * block_height
        image = image.resize((new_width, new_height))
        width, height = image.size
        print(f"调整图像尺寸为: {width}x{height}")
    
    pieces = []
    positions = []  # 记录每个小块的位置
    
    for i in range(rows):
        for j in range(cols):
            left = j * block_width
            upper = i * block_height
            right = left + block_width
            lower = upper + block_height
            
            piece = image.crop((left, upper, right, lower))
            pieces.append(piece)
            positions.append((i, j))  # (行, 列)
    
    return pieces, positions, (rows, cols)

def reconstruct_image_from_blocks(matched_blocks, positions, block_size, grid_size):
    """根据匹配结果重新构建图像"""
    rows, cols = grid_size
    block_width, block_height = block_size
    new_width = cols * block_width
    new_height = rows * block_height
    
    # 创建新的空白图像
    new_image = Image.new('RGB', (new_width, new_height))
    
    for (row, col), (block_path, rotation) in matched_blocks.items():
        if block_path:
            # 打开块图像
            block = Image.open(block_path)
            
            # 应用旋转
            if rotation != 0:
                block = block.rotate(-rotation, expand=True)
            
            # 调整大小以匹配块尺寸（确保和分割时大小一致）
            block = block.resize((block_width, block_height))
            
            # 计算位置并粘贴
            x = col * block_width
            y = row * block_height
            new_image.paste(block, (x, y))
            block.close()
    
    return new_image

def match_blocks_to_favicon(favicon_path, blocks_dir, output_path="reconstructed.png"):
    """将blocks目录中的所有块匹配到favicon.png"""
    
    # 1. 加载所有模型块
    print(f"正在加载模型块 from {blocks_dir}...")
    modelSamplings = []
    block_files = []
    block_size = None  # 用于记录模型块的尺寸
    
    if os.path.exists(blocks_dir):
        # 获取所有图像文件
        image_files = [f for f in os.listdir(blocks_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'))]
        
        print(f"找到 {len(image_files)} 个图像文件")
        
        for filename in image_files:
            filepath = os.path.join(blocks_dir, filename)
            try:
                img = Image.open(filepath)
                # 记录第一个模型块的尺寸，并假设所有模型块尺寸相同
                if block_size is None:
                    block_size = img.size  # (width, height)
                sample = NinePointSamplingAnalyze(img)
                modelSamplings.append({
                    "filename": filename,
                    "sample": sample,
                    "path": filepath
                })
                block_files.append(filepath)
            except Exception as e:
                print(f"无法处理文件 {filename}: {e}")
    else:
        raise FileNotFoundError(f"blocks 目录不存在: {blocks_dir}")

    if not modelSamplings:
        raise ValueError("未在 blocks 文件夹中找到任何有效图像！")
    
    print(f"成功加载 {len(modelSamplings)} 个模型块")
    print(f"模型块尺寸: {block_size}")
    
    # 2. 加载目标图像
    if not os.path.exists(favicon_path):
        raise FileNotFoundError(f"目标图像不存在: {favicon_path}")
    
    target_img = Image.open(favicon_path)
    target_width, target_height = target_img.size
    print(f"目标图像尺寸: {target_width}x{target_height}")
    
    # 3. 根据模型块尺寸分割目标图像
    if block_size is None:
        raise ValueError("无法确定模型块尺寸！")
    
    block_width, block_height = block_size
    cols = target_width // block_width
    rows = target_height // block_height
    
    print(f"将目标图像分割成 {rows} 行 {cols} 列，共 {rows*cols} 个小块")
    
    # 4. 分割目标图像
    print("正在分割目标图像...")
    target_pieces, positions, grid_size = split_image_by_block_size(target_img, block_width, block_height)
    print(f"分割成 {len(target_pieces)} 个小块")
    
    # 5. 对每个小块进行匹配
    print("正在匹配小块...")
    matched_blocks = {}
    used_blocks = set()  # 记录已使用的块，避免重复使用
    
    # 创建进度指示
    total_pieces = len(target_pieces)
    
    for idx, (piece, (row, col)) in enumerate(zip(target_pieces, positions)):
        # 显示进度
        if idx % 10 == 0 or idx == total_pieces - 1:
            print(f"  进度: {idx+1}/{total_pieces}")
        
        # 对当前小块进行采样
        piece_sample = NinePointSamplingAnalyze(piece.copy())
        
        # 寻找最佳匹配
        best_match_score = -1
        best_match_idx = -1
        best_rotation = 0
        
        # 在所有模型块中搜索（考虑是否允许重复使用）
        for model_idx, model in enumerate(modelSamplings):
            # 如果不想重复使用块，跳过已使用的
            if model_idx in used_blocks:
                continue
                
            score, rotation = SamplingBestRotate(model, piece_sample)
            if score > best_match_score:
                best_match_score = score
                best_match_idx = model_idx
                best_rotation = rotation
        
        # 记录匹配结果
        if best_match_idx >= 0:
            matched_blocks[(row, col)] = (
                modelSamplings[best_match_idx]["path"],
                best_rotation
            )
            used_blocks.add(best_match_idx)  # 标记为已使用
            
            if idx < 10:  # 只显示前10个匹配结果
                print(f"  位置({row},{col}): 匹配度 {best_match_score}/9, 旋转 {best_rotation}°, 文件 {modelSamplings[best_match_idx]['filename']}")
        else:
            print(f"  警告: 位置({row},{col}) 未找到匹配的块")
            matched_blocks[(row, col)] = (None, 0)
    
    print(f"匹配完成: {len(matched_blocks)}/{total_pieces} 个位置已匹配")
    
    # 6. 重新构建图像
    print("正在重新构建图像...")
    reconstructed = reconstruct_image_from_blocks(matched_blocks, positions, block_size, grid_size)
    
    # 7. 保存结果
    reconstructed.save(output_path)
    print(f"重构图像已保存到: {output_path}")
    
    # 显示原始和重构图像
    target_img.show(title="原始图像")
    reconstructed.show(title="重构图像")
    
    return reconstructed, matched_blocks

if __name__ == '__main__':
    # 设置路径
    blocks_dir = os.path.join("static", "img", "blocks")
    target_image_path = os.path.join("static", "img", "favicon.png")
    output_path = "reconstructed_favicon.png"
    
    try:
        result, matches = match_blocks_to_favicon(
            favicon_path=target_image_path,
            blocks_dir=blocks_dir,
            output_path=output_path
        )
        
        # 可选：生成匹配报告
        with open("matching_report.txt", "w") as f:
            f.write("拼图匹配报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"目标图像: {target_image_path}\n")
            f.write(f"模型块目录: {blocks_dir}\n")
            f.write(f"成功匹配位置数: {len([v for v in matches.values() if v[0]])}\n")
            f.write("\n详细匹配信息:\n")
            
            for (row, col), (path, rotation) in sorted(matches.items()):
                filename = os.path.basename(path) if path else "未匹配"
                f.write(f"位置({row},{col}): {filename} [旋转: {rotation}°]\n")
        
        print(f"匹配报告已保存到: matching_report.txt")
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
        import traceback
        traceback.print_exc()