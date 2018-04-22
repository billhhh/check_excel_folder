# Check excel and folders' names

import os
import pandas as pd
import numpy as np

# params
NUM_ROW = 1200;
excel_path = './excel/4_H365_Foods_for_LARC_HPB_Updated_20180422.xls';
DATA_PATH_ROOT = 'D:/dataset/FoodAI/Bill_Workspace/top50_confuse/FoodAI_756_20180422/val';

# read xls file
# 4, 18, 22 cols
df_i = pd.read_excel(excel_path, usecols=[1,4],sheet_name='Food_new', index_col=0, skiprows=0, header=0, skip_footer=0)[0:NUM_ROW];
df_v = pd.read_excel(excel_path, usecols=[1,18],sheet_name='Food_new', index_col=0, skiprows=0, header=0, skip_footer=0)[0:NUM_ROW];
df_c = pd.read_excel(excel_path, usecols=[1,22],sheet_name='Food_new', index_col=0, skiprows=0, header=0, skip_footer=0)[0:NUM_ROW];

ii = np.squeeze(df_i.as_matrix());
vv = np.squeeze(df_v.as_matrix());
cc = np.squeeze(df_c.as_matrix());

# STRIP FOR USE
for tmp in [ii, vv, cc]:
    for i in range(len(tmp)):
        # if type(tmp[i]) is not 'string':
            # print((tmp[i]))
            # print(type(tmp[i]))
        tmp[i] = tmp[i].strip().lower();

# i/v/c statistics
ii_set = set()
vv_set = set()
cc_set = set()
for item in ii:
    ii_set.add(str(item).lower().strip())
for item in vv:
    tmp = str(item).strip().lower()
    tmp = ''.join(tmp[0].upper() + tmp[1:])
    vv_set.add(tmp)
for item in cc:
    cc_set.add(str(item).lower().strip())

print('#item: ' + str(len(ii_set)))
print('#visual: ' + str(len(vv_set)))
print('#categories: ' + str(len(cc_set)))

# l2v_dict label to visual
l2v_dict={};
lb_set = set();
for item in vv_set:
    tmp = item.replace(' ', '_').replace('-', '_').replace('/', '_').replace("'", '_').lower();
    l2v_dict[tmp] = item;
    lb_set.add(tmp);
# print('l2v_dict', l2v_dict);
print('len l2v_dict', len(l2v_dict));

folder_label_names = list(filter(lambda x:x.endswith('.db')==False, os.listdir(DATA_PATH_ROOT)));
# for item in lb_set:
#     print(item)

print('------------------in folder not in excel')
for item in folder_label_names:
    if item not in lb_set:
        print(item)

print('------------------in excel not in folder')
for item in lb_set:
    if item not in folder_label_names:
        print(l2v_dict[item])