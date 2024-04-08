import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman' # 设置英文字体为Times New Roman
df = pd.read_csv('final_results.csv')#这里的data.csv为任意csv文件
df_corr = df.corr()#计算相关性系数
plt.figure(figsize=(10,8))#figsize可以规定热力图大小
plt.xticks(size=18,fontproperties='Times New Roman',weight='bold')
plt.yticks(size=18,fontproperties='Times New Roman',weight='bold')
fig = sns.heatmap(df_corr, #所绘数据
                  cmap='coolwarm', #颜色
                annot=True,fmt='.3g',#annot为热力图上显示数据；结果保留3位数字
                annot_kws={'size': 18, 'style': 'normal', #字体大小和格式
                           'family':'Times New Roman','weight': 'bold'}, #字体和风格--加粗
                linewidths=3, #图框分割线宽度
                square=True,  #使每个图框大小一致
                cbar = True) #绘制图例
cbar = fig.collections[0].colorbar
cbar.ax.tick_params(labelsize=20)  #设置图例字体大小
fig