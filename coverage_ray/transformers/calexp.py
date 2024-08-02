

# set_baseline=set()
# with open('/ct_log/可以用的data/6_27_jsonschema/6_27_jsonschema_test_*.py.txt','r') as baselinefile:
#   for line in baselinefile:
#     l=line.split(' ')[0]
#     set_baseline.add(l)



# with open('pyct_in_baseline.txt','w') as pyct_in_baselinefile:
#   with open('/ct_log/可以用的data/6_27_jsonschema/6_3_test_*.py_pyct.txt','r') as pyctfile:
#     for line in pyctfile:
#       l=line.split(' ')[0]
#       if l in set_baseline:
#         pyct_in_baselinefile.write(line)

# with open('baseline_in_pyctbaseline.txt','w') as baseline_in_pyctbaselinefile:
#   with open('/ct_log/可以用的data/6_27_jsonschema/6_7_test_*.py_no_pyct.txt','r') as baselinefile:
#     for line in baselinefile:
#       l=line.split(' ')[0]
#       if l in set_baseline:
#         baseline_in_pyctbaselinefile.write(line)

# set_pyct=set()
# with open('notCov.txt','w') as file:
#   with open('/ct_log/可以用的data/6_27_jsonschema/6_3_test_*.py_pyct.txt','r') as file1:
#     for line in file1:
#       l=line.split(' ')[0]
#       set_pyct.add(l)
#   with open('/ct_log/可以用的data/6_27_jsonschema/6_4_test_*.py.txt','r') as file2:
#     for line in file2:
#       l=line.split(' ')[0]
#       if l not in set_pyct:
#         file.write(line)

# cov=[]


# line=0
# with open('/ct_log/可以用的data/6_27_jsonschema/pyct_in_baseline.txt','r') as pyct_in_baselinefile:
#   for line in pyct_in_baselinefile:
#     words=[]
#     l=line.split(' ')
#     for c in l:
#       if c!='':
#         words.append(c)
#     cov.append(words)

# pyct_cov=[]


# line=0
# with open('/ct_log/可以用的data/6_27_jsonschema/6_3_test_*.py_pyct.txt','r') as pyctfile:
#   for line in pyctfile:
#     words=[]
#     l=line.split(' ')
#     for c in l:
#       if c!='':
#         words.append(c)
#     pyct_cov.append(words)

# baseline_cov=[]


# line=0
# with open('/ct_log/可以用的data/6_27_jsonschema/6_7_test_*.py_no_pyct.txt','r') as baselinefile:
#   for line in baselinefile:
#     words=[]
#     l=line.split(' ')
#     for c in l:
#       if c!='':
#         words.append(c)
#     baseline_cov.append(words)

# baseline_in_baseline_cov=[]


# line=0
# with open('/ct_log/可以用的data/6_27_jsonschema/baseline_in_pyctbaseline.txt','r') as baseline_in_pyctbaselinefile:
#   for line in baseline_in_pyctbaselinefile:
#     words=[]
#     l=line.split(' ')
#     for c in l:
#       if c!='':
#         words.append(c)
#     baseline_in_baseline_cov.append(words)

# for line in cov:
#   print(line)

# covLine=0
# notCovLine=0
# for line in cov:
#   if not line[0]=='TOTAL' and '-----' not in line[0] and line[1].isnumeric():
#     covLine+=int(line[1])
#   if not line[0]=='TOTAL' and '-----' not in line[0] and line[2].isnumeric():
#     notCovLine+=int(line[2])

# print(covLine)

# print(notCovLine)

# def split_except_whitespace(s):
#     words = []
#     word = ''
#     for char in s:
#         if char.isspace() and not word =='':
#             words.append(word)
#             print(word)
#             word = ''
#         else:
#             word += char
#     if word:
#         words.append(word)
#         print(words)
#     return words
# def list_to_csv(data):
#   import pandas as pd

#   # 示例数据：包含三个字段的列表
#   data = baseline_in_baseline_cov

#   # 将列表转换为 DataFrame
#   df = pd.DataFrame(data, columns=['Name', 'Stmts', 'Miss','cover'])

#   # 指定输出的 Excel 文件名
#   output_file = 'pyct_output.xlsx'

#   # 将 DataFrame 写入 Excel 文件
#   df.to_excel(output_file, index=False)

#   print(f"Data successfully written to {output_file}")

def cal_in_library(path,library_pattern):
  totalLine=0
  notCovLine=0
  package=set()
  module=set()
  with open(path,'r') as f:
    for line in f:
      words=[]
      # print(line.split(' '))
      l=line.split(' ')
      for c in l:
        if c!='':
          words.append(c)
      print(words)
      if library_pattern in words[0]:
        if not words[0]=='TOTAL' and '-----' not in words[0] and words[1].isnumeric():
          totalLine+=int(words[1])
        if not words[0]=='TOTAL' and '-----' not in words[0] and words[2].isnumeric():
          notCovLine+=int(words[2])

      start_index = words[0].find('/site-packages')
      if start_index != -1:
          start_index += len('/site-packages')
          end_index = words[0].find('/', start_index+1)
          if end_index != -1 and words[2]!=words[1]:
              sub_path = words[0][start_index:end_index]
              package.add(sub_path)
          if end_index != -1 and words[2]!=words[1]:
              start_index=end_index
              end_index = words[0].find('/', end_index+1)
              module.add(words[0][start_index:end_index])
    # print(words)
    print(f"total:{totalLine}")
    print(f"notcov:{notCovLine}")
    print(f"cov::{totalLine-notCovLine}")
    print(f"共{len(module)}個module")
    print(f"共{len(package)}個package")
    f.close()
if __name__=='__main__':
  cal_in_library('/home/soslab/pyct-coverage/coverage_ray/transformers/ct_log/可以用的data/6_3_test*.py_pyct/6_3_test_*.py_pyct.txt','/site-packages/transformers')
