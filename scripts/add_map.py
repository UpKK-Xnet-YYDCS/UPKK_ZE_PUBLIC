import vdf
import argparse
import os

def add_map_to_file(file_path, map_name, workshop_id):
    """
    向指定的 Valve KeyValue 格式文件添加新的地图数据。如果地图已存在，则忽略。
    
    参数:
        file_path (str): KeyValue 文件路径
        map_name (str): 地图名称
        workshop_id (str): 工作坊 ID
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")

        # 读取 KeyValue 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = vdf.load(file)
            except Exception as e:
                raise ValueError(f"无法解析 KeyValue 文件: {str(e)}")

        # 确保 Maplist 键存在
        if "Maplist" not in data:
            data["Maplist"] = {}

        # 检查地图是否已存在
        if map_name in data["Maplist"]:
            print(f"地图 {map_name} 已存在，跳过添加")
            return

        # 创建新地图数据，使用默认值
        new_map = {
            "workshop_id": workshop_id,
            "enabled": "1",
            "filename": map_name,
            "updatedname": map_name,
            "OnlyNominate": "0"
        }

        # 添加新地图到 Maplist
        data["Maplist"][map_name] = new_map

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            vdf.dump(data, file, pretty=True)
        
        print(f"成功添加地图 {map_name} 到 {file_path}")

    except Exception as e:
        print(f"错误: {str(e)}")

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="向 Valve KeyValue 格式的 Maplist 文件添加新地图")
    parser.add_argument("file_path", help="Maplist 文件路径")
    parser.add_argument("map_name", help="地图名称")
    parser.add_argument("workshop_id", help="工作坊 ID")

    # 解析参数
    args = parser.parse_args()

    # 调用添加地图函数
    add_map_to_file(args.file_path, args.map_name, args.workshop_id)

if __name__ == "__main__":
    main()