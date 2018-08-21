# blogtagging
2018.07.24 Ver.

## Setup Website
```
python3 main.py
```
## Data Reorder
```
python3 dataReorder.py --alluser --n_user $N_USER     # 生出所有 users 的進度到 generated_csv/alluser_analysis.csv 裡
python3 dataReorder.py --organize --n_user $N_USER    # 彙整 userData/ 裡的所有tagged data 到 doneData/ 中
python3 dataReorder.py --count                        # 整理 doneData/ 中各分類並統計至 generated_csv/
```
