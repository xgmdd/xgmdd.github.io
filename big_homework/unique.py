import pandas as pd
import os
from processdata import get_total_times
def unique_segment(day:int,num:int):

    """接受天数和页数，去重处理./output/tables/segment下的csv文件
    再生成./output/tables/segment-p下的csv文件"""

    # 输入输出文件名
    src_filename = './output/tables/segment/day{}/page_{}.csv'.format(day,num)
    dest_filename = './output/tables/segment-p/day{}/page_{}.csv'.format(day,num)
    # 确保文件名路径有效
    if not os.path.exists('./output/tables/segment-p/day{}'.format(day)):
        os.makedirs('./output/tables/segment-p/day{}'.format(day))
    # 读取数据
    df = pd.read_csv(src_filename,dtype=str) 
    # print(df.shape[0]) 1058
    # 转化为字典格式
    pairs={(df['seg_from'][i],df['seg_to'][i]):df['color'][i] for i in range(df.shape[0])}
    # 新字典作为去重操作后的
    new_pairs = {}
    {new_pairs.update({key:pairs[key]}) for key in pairs if key not in new_pairs.keys()}
    # print(len(new_pairs)) 922
    # 写入新文件
    f=open(dest_filename,'w',encoding='utf-8')
    # 写表头
    f.write('from,to,color\n')
    # 遍历字典
    for key in new_pairs:
        f.write(key[0]+','+key[1]+','+new_pairs[key]+'\n')
    f.close()
    # print("done"+str(num))
def unique_station(day:int,num:int):

    """接受天数和页数，去重处理./output/tables/station下的csv文件
    再生成./output/tables/station-p下的csv文件"""

    # 输入输出文件名
    src_filename = './output/tables/station/day{}/page_{}.csv'.format(day,num)
    dest_filename = './output/tables/station-p/day{}/page_{}.csv'.format(day,num)
    # 确保文件名路径有效
    if not os.path.exists('./output/tables/station-p/day{}'.format(day)):
        os.makedirs('./output/tables/station-p/day{}'.format(day))
    # 读取数据
    df = pd.read_csv(src_filename,dtype=str) 
    # print(df.shape[0]) 1058
    # 转化为字典格式
    pairs={df['name'][i]:df['color'][i] for i in range(df.shape[0])}
    # 新字典作为去重操作后的
    new_pairs = {}
    {new_pairs.update({key:pairs[key]}) for key in pairs if key not in new_pairs.keys()}
    # print(len(new_pairs)) 922
    # 写入新文件
    f=open(dest_filename,'w',encoding='utf-8')
    # 写表头
    f.write('name,color\n')
    # 遍历字典
    for key in new_pairs:
        f.write(key+','+new_pairs[key]+'\n')
    f.close()
    # print("done"+str(num))
# test
for day in range(6):
    for i in range(get_total_times(day)):
        unique_station(day,i)  
        unique_segment(day,i) 
    print("done uniquelize day{}".format(day))