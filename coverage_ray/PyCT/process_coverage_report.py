import pandas as pd

def combine_coverage_report(fp, keep_prefix=None):
    data = open(fp).read()
    
    # 按行分割文本数据
    lines = data.strip().split("\n")

    # 提取列名
    columns = lines[0].split()

    # 提取数据行
    data_lines = [line for line in lines[2:] if line.strip()]

    # 将数据行转换为二维列表
    data_list = [line.split() for line in data_lines]

    # 创建 DataFrame
    df = pd.DataFrame(data_list, columns=columns)

    # 去除重复的标题行
    df = df[df['Name'] != 'Name']

    # 去除不需要的 "TOTAL" 列
    df = df[~df['Name'].str.contains("TOTAL")]
    
    # 只保留prefix開頭的紀錄
    if keep_prefix:
        df = df[df['Name'].str.startswith(keep_prefix)]

    # 重置索引
    df.dropna(axis=0, inplace=True)

    # 同樣的py檔，只保留miss最小的紀錄
    df = df.sort_values('Miss').groupby('Name').first().reset_index()

    df.reset_index(drop=True, inplace=True)

    # 打印 DataFrame
    print(df)
    
    return df
    

# combine_coverage_report('part_report.txt', keep_prefix='transformers')
report_df = combine_coverage_report('test_coverage_report.txt', keep_prefix='transformers')
report_df['Stmts'] = report_df['Stmts'].astype(int)
report_df['Miss'] = report_df['Miss'].astype(int)
total_line = report_df['Stmts'].sum()
miss_line = report_df['Miss'].sum()

coverage = (total_line - miss_line) / total_line
print(total_line, miss_line, coverage)


# data = """
# Name    Stmts   Miss  Cover
# ---------------------------
# transformers/src/transformers/image_processing_utils.py      182    142    22%
# transformers/src/transformers/utils/doc.py                   177    173     2%
# transformers/src/transformers/utils/logging.py               140    134     4%
# ------------------------------------------------------------------------------
# TOTAL                                                       1133    903    20%
# Name                                                                           Stmts   Miss  Cover
# --------------------------------------------------------------------------------------------------
# transformers/src/transformers/convert_slow_tokenizers_checkpoints_to_fast.py      57     46    19%
# transformers/src/transformers/utils/logging.py                                   140    129     8%
# --------------------------------------------------------------------------------------------------
# TOTAL                                                                           1413   1210    14%
# """

# # 按行分割文本数据
# lines = data.strip().split("\n")

# # 提取列名
# columns = lines[0].split()

# # 提取数据行
# data_lines = [line for line in lines[2:] if line.strip()]

# # 将数据行转换为二维列表
# data_list = [line.split() for line in data_lines]

# # 创建 DataFrame
# df = pd.DataFrame(data_list, columns=columns)

# # 去除重复的标题行
# df = df[df['Name'] != 'Name']

# # 去除不需要的 "TOTAL" 列
# df = df[~df['Name'].str.contains("TOTAL")]

# # 重置索引
# df.dropna(axis=0, inplace=True)

# # 同樣的py檔，只保留miss最小的紀錄
# df = df.sort_values('Miss').groupby('Name').first().reset_index()

# df.reset_index(drop=True, inplace=True)

# # 打印 DataFrame
# print(df)