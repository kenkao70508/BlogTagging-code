# blogtagging
2018.07.24 Ver.

## Setup Website
```
python3 main.py
```
## Data Reorder
- Organize Data
- Track User's Progress
- Tagged Articles Statistics

### Track User's Progress
```
python3 dataReorder.py --alluser --n_user $N_USER     # 生出所有 users 的進度到 generated_csv/alluser_analysis.csv 裡
```
### Organize Data
```
python3 dataReorder.py --organize --n_user $N_USER    # 彙整 userData/ 裡的所有tagged data 到 doneData/ 中
```
### Get Tagged Articles' Statistics
```
python3 dataReorder.py --statistics                   # 整理 doneData/ 中各分類並統計至 generated_csv/
```
