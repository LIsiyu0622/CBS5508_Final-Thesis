import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 从CSV文件加载数据
tea_books = pd.read_csv('tea_book.csv')

# 从数据中过滤掉'Shilinhuangji'
tea_books = tea_books[tea_books['BookTitle'] != 'Shilinhuangji']

# 为每本书定义更好的颜色
book_colors = {
    'Chajing': '#ff9999',           # 粉红色
    'Daguanchalun': '#b3cc33',      # 黄绿色
    'Chalu': '#66cc66',             # 绿色
    'Pinchayaolu': '#33ccaa',       # 青绿色
    'Chapu': '#3399cc',             # 青色
    'Chashu': '#3366cc',            # 蓝色
    'Chaliaoji': '#9966cc',         # 紫色
    'Zhuquanxiaopin': '#ff66cc'     # 洋红色
}

# 确保所有书籍都有颜色
for book in tea_books['BookTitle'].unique():
    if book not in book_colors:
        book_colors[book] = '#999999'  # 默认灰色

# 设置朝代顺序
dynasty_order = {'Tang': 0, 'Song': 1, 'Ming': 2}
tea_books['DynastyOrder'] = tea_books['Dynasty'].map(dynasty_order)

# 计算每本书的朝代
book_dynasties = {}
for book in tea_books['BookTitle'].unique():
    dynasty = tea_books[tea_books['BookTitle'] == book]['Dynasty'].iloc[0]
    book_dynasties[book] = dynasty

# 按朝代排序书籍
sorted_books = sorted(book_dynasties.items(), key=lambda x: dynasty_order.get(x[1], 999))
book_order = [book for book, _ in sorted_books]

# 创建画布
plt.figure(figsize=(14, 8))
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# 设置背景颜色为浅灰色
plt.gca().set_facecolor('#f8f8f8')

# 创建小提琴图
ax = sns.violinplot(
    x='BookTitle', 
    y='TokenCount', 
    data=tea_books,
    order=book_order,
    palette=book_colors,
    inner='box',     # 显示箱线图
    linewidth=1.0,   # 减小线宽
    cut=0,           # 重要: 不截断分布
    scale='width',   # 同等宽度
    width=0.8,       # 小提琴图宽度
)

# 设置y轴范围，确保完整显示
y_max = tea_books['TokenCount'].max() * 1.1  # 增加10%空间
plt.ylim(0, y_max)

# 添加标题和轴标签
plt.title("Token Count Distribution by Book", fontsize=16, fontweight='bold', pad=20)
plt.xlabel("Book Title", fontsize=12, labelpad=10)
plt.ylabel("Token Count", fontsize=12, labelpad=10)

# 添加每本书的统计信息
for i, book in enumerate(book_order):
    book_data = tea_books[tea_books['BookTitle'] == book]
    chapter_count = len(book_data)
    avg_tokens = int(book_data['TokenCount'].mean())
    
    # 在小提琴图下方添加信息
    plt.text(i, -y_max*0.05, 
             f"n={chapter_count}\nμ={avg_tokens}", 
             ha='center', 
             va='top', 
             fontsize=8,
             color='#333333')

# 为不同朝代添加标记
dynasty_groups = {}
for i, book in enumerate(book_order):
    dynasty = book_dynasties[book]
    if dynasty not in dynasty_groups:
        dynasty_groups[dynasty] = []
    dynasty_groups[dynasty].append(i)

dynasty_colors = {'Tang': '#ffeeee', 'Song': '#eeffee', 'Ming': '#eeeeff'}

# 在背景添加朝代区域
for dynasty, indices in dynasty_groups.items():
    if indices:
        start = min(indices) - 0.5
        end = max(indices) + 0.5
        plt.axvspan(start, end, alpha=0.3, color=dynasty_colors.get(dynasty, '#f0f0f0'))
        
        # 添加朝代标签
        plt.text((start + end) / 2, y_max * 0.95, 
                dynasty, 
                ha='center', 
                va='top', 
                fontsize=12, 
                fontweight='bold',
                color='#555555',
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

# 美化图表
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

# 添加解释文本
plt.figtext(0.5, 0.01, 
           "Note: Violin plots show the distribution of token counts across chapters. Wider sections indicate more chapters with that token count. Box plots show median and quartiles.",
           ha='center', fontsize=9, style='italic')

# 调整布局并保存
plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.savefig('tea_books_token_distribution.png', dpi=300, bbox_inches='tight')
plt.show()