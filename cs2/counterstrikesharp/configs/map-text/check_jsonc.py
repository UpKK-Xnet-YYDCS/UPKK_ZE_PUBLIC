# check_jsonc.py
import json
import os
import shutil
from pathlib import Path

# 需要支持 // 注释 的 jsonc 解析（推荐用这个库）
try:
    import commentjson
except ImportError:
    print("请先安装 commentjson 库：")
    print("   pip install commentjson")
    exit(1)

def is_valid_jsonc(filepath: str | Path) -> bool:
    """尝试解析 jsonc 文件，成功返回 True"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            commentjson.load(f)
        return True
    except commentjson.JSONLibraryException as e:
        print(f"× 非法 JSONC: {filepath}")
        print(f"  错误: {e}")
        return False
    except Exception as e:
        print(f"× 读取/解析失败: {filepath}")
        print(f"  异常: {type(e).__name__}: {e}")
        return False


def main():
    current_dir = Path.cwd()
    failed_dir = current_dir / "failed"
    
    # 创建 failed 文件夹（如果不存在）
    failed_dir.mkdir(exist_ok=True)
    
    moved_count = 0
    total_files = 0
    
    print(f"正在检查目录: {current_dir}\n")
    
    # 遍历当前目录下所有 .jsonc 文件（不递归子文件夹）
    for file_path in current_dir.glob("*.jsonc"):
        total_files += 1
        if is_valid_jsonc(file_path):
            print(f"✓ 通过: {file_path.name}")
        else:
            # 移动到 failed/ 目录
            target_path = failed_dir / file_path.name
            # 如果同名文件已存在，加 (1)、(2)... 后缀
            counter = 1
            while target_path.exists():
                stem = file_path.stem
                target_path = failed_dir / f"{stem} ({counter}){file_path.suffix}"
                counter += 1
                
            shutil.move(file_path, target_path)
            print(f"  → 已移动到: failed/{target_path.name}")
            moved_count += 1
    
    print("\n" + "="*50)
    print(f"检查完成！共发现 {total_files} 个 .jsonc 文件")
    print(f"合法文件   : {total_files - moved_count} 个")
    print(f"非法并移动 : {moved_count} 个 → failed/ 目录")
    if moved_count > 0:
        print(f"失败文件存放路径: {failed_dir}")


if __name__ == "__main__":
    main()