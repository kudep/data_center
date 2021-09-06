# `DataSpot`

`DataSpot` provides convenient work with data on disk space in python.

# Links
[Github](https://github.com/kudep/data_spot)

# Quick Start

## Installation
```bash
pip install git+https://github.com/kudep/data_spot.git@dev
```

## Use `DataSpot` 
Create `DataSpot` for `/tmp/work_dir/` directory and saving/getting data by `DataSpot`.
```python
from data_spot import DataSpot


dc1 = DataSpot("/tmp/work_dir/")
# save data to Data Spot
dc1["data1"] = {"1": [1, 2, 3, 4], "2": {"13": 1, "21": 2}}
dc1["123"] = 123
print(f"{dc1.keys()=}") # returns `dc1.keys()=dict_keys(['123', 'data1'])`
print(f"{list(dc1.items())=}") # returns `list(dc1.items())=[('123', 123), ('data1', {'1': [1, 2, 3, 4], '2': {'13': 1, '21': 2}})]`
print(f"{dc1['data1']=}") # returns `ddc1['data1']={'1': [1, 2, 3, 4], '2': {'13': 1, '21': 2}}`
```
Updates of `/tmp/work_dir/`
```bash
tree -L 2 /tmp/work_dir/
# /tmp/work_dir/
# ├── 123.o.pkl.dc
# └── data1.o.pkl.dc
# 0 directories, 2 files
```
Deleting objects from `DataSpot`
```python
from data_spot import DataSpot


dc1 = DataSpot("/tmp/work_dir/")
del dc1["data1"]
del dc1["123"]
```
Updates of `/tmp/work_dir/`
```bash
tree -L 2 /tmp/work_dir/
# /tmp/work_dir/
# 0 directories, 0 files
```
Using `pandas`/`Series`/`numpy` with `DataSpot`
```python
from data_spot import DataSpot
import pandas as pd
import numpy as np


dc1 = DataSpot("/tmp/work_dir/")
dc1["data_frame"] = pd.DataFrame({})
dc1["range"] = pd.Series([1,2,3,4])
dc1["ones"] = np.ones([10,40,60,70])

```
Updates of `/tmp/work_dir/`
```bash
tree -L 2 /tmp/work_dir/
# /tmp/work_dir/
# ├── data_frame.df.parquet.dc
# ├── ones.np.parquet.dc
# └── range.sr.parquet.dc

# 0 directories, 3 files

```
Deleting all objects from `DataSpot`
```python
from data_spot import DataSpot


dc1 = DataSpot("/tmp/work_dir/")
dc1.clear()
```
Updates of `/tmp/work_dir/`
```bash
tree -L 2 /tmp/work_dir/
# /tmp/work_dir/
# 0 directories, 0 files
```


## Use many `DataSpot`s 
Create `DataSpot` for `/tmp/work_dir` directory and saving/getting data by `DataSpot`.
```python
from data_spot import DataSpot


dc1 = DataSpot("/tmp/work_dir")
# create new DataSpot and it's called `dc2`
dc2 = dc1.dcs.get("dc2")
print(f"{dc1.dcs.keys()=}") # returns `dc1.dcs.keys()=dict_keys(['dc2'])`
# get created DataSpot `dc2` from Data Spot `dc1`
dc2 = dc1.dcs["dc2"]
# dc2["df"] = pd.DataFrame({1: [1, 2, 3, 4]})
dc2["variable"] = 123
print(f"{dc2['variable']=}") # returns `dc2['variable']=123`
print(f"{list(dc2.items())=}") # returns `list(dc2.items())=[('variable', 123)]`
```

```bash
tree -L 2 /tmp/work_dir/
# /tmp/work_dir/
# └── dc2
#     └── variable.o.pkl.dc
# 1 directory, 1 files
```
# Contributing to `DataSpot`

Please refer to [CONTRIBUTING.md](https://github.com/kudep/data_spot/dev/CONTRIBUTING.md).