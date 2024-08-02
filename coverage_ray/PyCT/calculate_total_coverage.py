import os
from pathlib import Path
from collections import defaultdict
import pandas as pd

STATS_DIR = "project_statistics"

# target_project = 'django'
# target_project = 'django_4.1_src'

target_project = 'transformers'

total_dict = defaultdict(list)

for ctxt in Path(os.path.join(STATS_DIR, target_project)).rglob("coverage.txt"):
    module = ctxt.parent.parent.name
    function = ctxt.parent.name
    
    with open(ctxt, 'r') as f:
        line = f.readline()
        slash_idx = line.index('/')
        num_cover_line = int(line[:slash_idx])
        num_total_line = int(line[slash_idx+1: line.index(' ')]) 
        # print(line, num_cover_line, num_total_line)
    
    # print(module, function)
    
    total_dict['module'].append(module)
    total_dict['function'].append(function)
    total_dict['cover_line'].append(num_cover_line)
    total_dict['total_line'].append(num_total_line)
    

res = pd.DataFrame(total_dict)

total_cover_line = res['cover_line'].sum()
total_total_line = res['total_line'].sum()

print(target_project, 'coverage:', end=' ')
print(f"{total_cover_line} / {total_total_line} = {total_cover_line / total_total_line:.6f}")


# ver = 4.2 py38
# django coverage: 2642 / 5336 = 0.495127

# ver = 4.1 py38
# django coverage: 31859 / 75003 = 0.424770

# ver = 4.1 py38 - django/django
# django_4.1_src coverage: 12471 / 32936 = 0.378643

# ver = 4.28.1 py38
# transformers coverage: 692 / 1880 = 0.368085
# transformers coverage: 9246 / 42804 = 0.216008
