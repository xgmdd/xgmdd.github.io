import pandas as pd
df=pd.read_csv("./output/tables/station-p/day0/page_1.csv",encoding='utf-8')
df['name'].to_csv('./data/names.csv')

import jieba

txt_filename = './data/names.csv'
result_filename = './output/freq.csv'



# 从文件读取文本
txt_file = open(txt_filename, 'r', encoding='utf-8')
content = txt_file.read()
txt_file.close()

# 分词
word_list = jieba.lcut(content)

# 用字典统计每个词的出现次数
word_dict = {}
for w in word_list:
    try:
        int(w)
    except:
        if w==',' or w=='\n' or w=='name':
            continue
        if w in word_dict.keys():
            word_dict[w] = word_dict[w] + 1
        else:
            word_dict[w] = 1


# 把字典转成列表，并按原先“键值对”中的“值”从大到小排序
items_list = list(word_dict.items())
items_list.sort(key=lambda x:x[1], reverse=True)

total_num = len(items_list)
print('经统计，共有' + str(total_num) + '个不同的词')

# 根据用户需求，打印排名前列的词，同时把统计结果存入文件
num = input('您想查看前多少个？[10]:')
if not num.isdigit() or num == '': # 如果输入的不全是数字，或者直接按了回车
    num = 10  # 设成查看前10名
else:
    num = int(num)  # 如果输入了正常的数字，则按用户需求设置

result_file = open(result_filename, 'w',encoding='utf-8')   # 新建结果文件

result_file.write('word,出现次数\n')  # 写入标题行

for i in range(num):
    word, cnt = items_list[i]
    message = str(i+1) + '. ' + word + '\t' + str(cnt)
    print(message)
    result_file.write(word + ',' + str(cnt) + '\n')
    
result_file.close()  # 关闭文件

print('已写入文件：' + result_filename)

from pyecharts import options as opts
from pyecharts.charts import WordCloud

##-------从文件中读出人物词频------------------
src_filename = './output/freq.csv'
# 格式：人物,出现次数

src_file = open(src_filename, 'r',encoding='utf-8')
line_list = src_file.readlines()  #返回列表，文件中的一行是一个元素
src_file.close()

wordfreq_list = []  #用于保存元组(人物姓名,出现次数)
for line in line_list:
    line = line.strip()  #删除'\n'
    line_split = line.split(',')
    wordfreq_list.append((line_split[0],line_split[1]))

del wordfreq_list[0] #删除csv文件中的标题行
print('word数量：' + str(len(wordfreq_list)))
##-------从文件中读出人物词频完成------------------

##===============================================
##-------生成词云---------------------------------
cloud = WordCloud()

# 设置词云图
cloud.add('', 
          wordfreq_list[0:90], #元组列表，词和词频
          shape='diamond', # 轮廓形状：'circle','cardioid','diamond',
                           # 'triangle-forward','triangle','pentagon','star'
          # mask_image='./data/词云背景图-中国.jpg', # 轮廓图，第一次显示可能有问题，刷新即可
          is_draw_out_of_bound=False, #允许词云超出画布边界
          word_size_range=[10, 60], #字体大小范围
          textstyle_opts=opts.TextStyleOpts(font_family="华文行楷"),
          #字体：例如，微软雅黑，宋体，华文行楷，Arial
          )

# 设置标题
cloud.set_global_opts(title_opts=opts.TitleOpts(title="地铁站名成分词云"))

# render会生成HTML文件。默认是当前目录render.html，也可以指定文件名参数
out_filename = './charts/wordcloud_opts.html'
cloud.render(out_filename)

print('生成结果文件：' + out_filename)