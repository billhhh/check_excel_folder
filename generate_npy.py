# Check excel and folders' names

import os
import pandas as pd
import numpy as np
import operator

# params
NUM_ROW = 1200;
SAVE_FLAG = False;
excel_path = './excel/5_H365_Foods_for_LARC_HPB_Updated_20180422.xls';

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

# v2ci_dict
v2ci_dict={}
# for statistical purpose
i2c_dict = {}
i2v_dict = {}
for i in range(len(ii)):
    tmp_i = ii[i]
    tmp_v = vv[i]
    tmp_c = cc[i]

    tmp_i = ''.join(tmp_i[0].upper() + tmp_i[1:])
    tmp_v = ''.join(tmp_v[0].upper() + tmp_v[1:])
    tmp_c = ''.join(tmp_c[0].upper() + tmp_c[1:])

    i2v_dict[tmp_i] = tmp_v
    i2c_dict[tmp_i] = tmp_c

    if tmp_v not in v2ci_dict:
        v2ci_dict[tmp_v] = {tmp_c:[tmp_i]}
    #visual food in dict
    else:
        # visual food more than one cat: new?
        if tmp_c not in v2ci_dict[tmp_v]:
            v2ci_dict[tmp_v].update({tmp_c:[tmp_i]})
        else:
            v2ci_dict[tmp_v][tmp_c].append(tmp_i)

print(v2ci_dict)
# for i in v2ci_dict:
#     print(i)
#     print(v2ci_dict[i])

if SAVE_FLAG:
    # SAVE l2v_dict
    np.save('l2v_dict.npy',l2v_dict)
    with open('l2v_dict.txt','w') as f:
        for item in l2v_dict:
            f.write(item + ':'+l2v_dict[item]+'\n')

    # SAVE v2ci_dict
    np.save('v2ci_dict.npy',v2ci_dict)
    with open('v2ci_dict.txt','w') as f:
        f.write('VISUAL NAME\n\tCATEGORY NAME\n\t\tITEM NAME\n')
        f.write('-' * 50 + '\n')
        for item in v2ci_dict:
            f.write(item + ': \n')
            tmp_dict = v2ci_dict[item]
            for item_i in tmp_dict:
                f.write('\t'+item_i + '\n')
                for item_ii in tmp_dict[item_i]:
                    f.write('\t\t'+item_ii+'\n')
    cnt=0
    with open('v2ci_dict_more.txt','w') as f:
        f.write('VISUAL NAME\n\tCATEGORY NAME\n\t\tITEM NAME\n')
        f.write('-' * 50 + '\n')
        for item in v2ci_dict:
            if len(v2ci_dict[item]) > 1:
                cnt+=1
                f.write(item + ': \n')
                tmp_dict = v2ci_dict[item]
                for item_i in tmp_dict:
                    f.write('\t'+item_i + '\n')
                    for item_ii in tmp_dict[item_i]:
                        f.write('\t\t'+item_ii+'\n')
    print('visual food more than one cat: %d'%cnt)

    # v to i count
    i2v_dict_cnt={}
    for i in i2v_dict:
        c = i2v_dict[i]
        if c not in i2v_dict_cnt:
            i2v_dict_cnt[c] = 1
        else:
            i2v_dict_cnt[c]+=1
    with open('v2i_cnt_dict.txt', 'w') as f:
        f.write('%-50s:\t%s\n'%('VISUAL NAME','#ITEMS'))
        f.write('%-50s\n'%('-'*60))
        for t in sorted(i2v_dict_cnt.items(), key=operator.itemgetter(1)):
            f.write('%-50s:\t%d\n'%(t[0],t[1]))

    # c to i count
    i2c_dict_cnt={}
    for i in i2c_dict:
        c = i2c_dict[i]
        if c not in i2c_dict_cnt:
            i2c_dict_cnt[c] = 1
        else:
            i2c_dict_cnt[c]+=1
    with open('c2i_cnt_dict.txt', 'w') as f:
        f.write('%-50s:\t%s\n'%('CATEGORY NAME','#ITEMS'))
        f.write('%-50s\n'%('-'*60))
        for t in sorted(i2c_dict_cnt.items(), key=operator.itemgetter(1)):
            f.write('%-50s:\t%d\n'%(t[0],t[1]))
