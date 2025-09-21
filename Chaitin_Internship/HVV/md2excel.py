import pandas as pd
from io import StringIO

# Markdown 表格数据
with open('week.md', 'r') as file:
    markdown_table = file.read()

# 使用pandas读取Markdown表格
data = pd.read_csv(StringIO(markdown_table), sep="|", engine='python').iloc[1:]
# 保存为Excel文件
data.to_excel('attacks.xlsx', index=False)