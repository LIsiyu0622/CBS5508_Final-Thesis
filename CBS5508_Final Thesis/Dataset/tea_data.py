import os
import json

def process_tea_data(root_folder, output_json_path):
    data = []
    
    # 遍历朝代文件夹
    for dynasty in os.listdir(root_folder):
        dynasty_folder = os.path.join(root_folder, dynasty)
        if os.path.isdir(dynasty_folder):
            # 遍历每个朝代文件夹中的所有文本文件
            for file_name in os.listdir(dynasty_folder):
                if file_name.endswith('_filtered.txt'):
                    file_path = os.path.join(dynasty_folder, file_name)
                    # 提取文件名前缀作为作品名称
                    work_name = file_name.replace('_filtered.txt', '')
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # 按行分割文本，假设每行是一个独立的样本
                        lines = content.strip().split('\n')
                        for line in lines:
                            if line.strip():  # 跳过空行
                                # 创建数据项，包含朝代和作品信息
                                data_item = {
                                    "text": line,
                                    "dynasty": dynasty,
                                    "work": work_name
                                }
                                data.append(data_item)
    
    # 将数据保存为JSON文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已处理 {len(data)} 条数据，涵盖 {len(set(item['dynasty'] for item in data))} 个朝代")
    print(f"数据已保存至 {output_json_path}")

# 使用示例
process_tea_data('C:\Users\lisiy\TeaBooks_Intertextuality_Modeling\data\chashu_filtered', './data/tea_data.json')