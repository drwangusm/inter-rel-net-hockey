import pandas as pd
import matplotlib.pyplot as plt

# 加载数据
data = pd.read_csv('final_results.csv')

# 提取模型名称和评估指标数据
models = data['model']
accuracy = data['val_acc_mean']
recall = data['val_recall_mean']
precision = data['val_precision_mean']
f1 = data['val_f1_mean']

# 绘制柱状图
plt.figure(figsize=(16, 12))
plt.bar(models, accuracy, label='Accuracy')
plt.bar(models, recall, label='Recall')
plt.bar(models, precision, label='Precision')
plt.bar(models, f1, label='F1')
plt.xlabel('Model')
plt.ylabel('Score')
plt.title('Evaluation Metrics for Different Models')
plt.xticks(rotation=90)
plt.legend()
plt.savefig("hist.png")
plt.show()

# 绘制折线图
plt.figure(figsize=(16, 12))
plt.plot(models, accuracy, marker='o', label='Accuracy')
plt.plot(models, recall, marker='o', label='Recall')
plt.plot(models, precision, marker='o', label='Precision')
plt.plot(models, f1, marker='o', label='F1')
plt.xlabel('Model')
plt.ylabel('Score')
plt.title('Evaluation Metrics for Different Models')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.savefig("pr.png")
plt.show()

import seaborn as sns

# 设置索引为模型名称
data.set_index('model', inplace=True)

# 绘制热力图
plt.figure(figsize=(16, 12))
sns.heatmap(data, annot=True, cmap='YlGnBu', fmt=".2f")
plt.title('Evaluation Metrics for Different Models')
plt.xlabel('Metrics')
plt.ylabel('Model')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.savefig("matrix.png")
plt.show()




