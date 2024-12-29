import numpy as np
import pandas as pd
import os
import openpyxl

if __name__ == '__main__':
    
    # 讀取答案資料
    file_path = 'data/107-108大腸癌整合好(給高科大).xlsx'
    data = pd.read_excel(file_path)
    
    def get_file_names(directory):
        return [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    base_dir = 'data'
    sub_dirs = ['復發', '無復發',"一直存在"]
    file_dict = {}

    # 讀取病理報告資料並將復發資訊填入
    for sub_dir in sub_dirs:
        dir_path = os.path.join(base_dir, sub_dir)
        file_dict[sub_dir] = get_file_names(dir_path)

    print(file_dict)
    def read_ids_from_files(directory, filenames):
        ids = set()
        for filename in filenames:
            file_path = os.path.join(directory, filename)
            if filename.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif filename.endswith('.xls'):
                df = pd.read_excel(file_path, engine='xlrd')
            
            ids.update(df['ID'].tolist())
        return ids

    file_names = ['check.xlsx', 'opd.xlsx', 'path.xls']
    id_dict = {}

    for sub_dir in sub_dirs:
        dir_path = os.path.join(base_dir, sub_dir)
        id_dict[sub_dir] = read_ids_from_files(dir_path, file_names)

    # 比對 id_dict 的 value 倆倆有沒有重複
    for key1, ids1 in id_dict.items():
        for key2, ids2 in id_dict.items():
            if key1 != key2:
                common_ids = ids1.intersection(ids2)
                if common_ids:
                    print(f"Common IDs between {key1} and {key2}: {common_ids}")
    
    
    # 將復發資訊填入答案資料
    data['復發資訊'] = np.nan

    for sub_dir, ids in id_dict.items():
        data.loc[data['ID'].isin(ids), '復發資訊'] = sub_dir

    total_counts = {sub_dir: len(ids) for sub_dir, ids in id_dict.items()}
    missing_info_count = len(data[data['復發資訊'].isna()])

    print("Total counts per category:", total_counts)
    print("Count of IDs in answer data but missing recurrence info:", missing_info_count)
    
    # 將整合好的資料存成新的 Excel 檔
    new_file_path = 'data/answer.xlsx'
    data.to_excel(new_file_path, index=False)
    