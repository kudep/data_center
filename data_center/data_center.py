from typing import Union, Any

import pathlib
import pickle
import logging
import json

import traceback

logger = logging.getLogger(__name__)

try:
    import pandas as pd
except Exception:
    pd = False

try:
    import numpy as np
except Exception:
    np = False


class DataCenter:
    def __init__(self, root: Union[pathlib.Path, str]):
        self.root = pathlib.Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.name = self.root.name
        self.dcs = DataCenters(self.root)

    def _map(self):
        return {file.name.replace("".join(file.suffixes), ""): file for file in self.root.glob("*.dc")}

    def keys(self):
        return self._map().keys()

    def __getitem__(self, key):
        file = self._map()[key]
        data_format, file_format = file.suffixes[:2]
        if file_format == ".parquet":
            df = pd.read_parquet(file)
            if data_format in [".np"]:
                shape = json.loads(df.columns[0])
                return df.iloc[:, 0].values.reshape(shape)
            elif data_format in [".sr"]:
                return df["data"]
            elif data_format in [".df"]:
                return df
            else:
                raise Exception(f"Unknown data type {file}")
        elif file_format == ".pkl":
            obj = pickle.load(file.open("rb"))
            if data_format in [".o"]:
                return obj
            else:
                raise Exception(f"Unknown data type {file}")
        else:
            raise Exception(f"Unknown file type {file}")

    def get(self, key: str, default: Any = None, verbose: bool = False):
        try:
            return self.__getitem__(key)
        except Exception:
            if verbose:
                logger.warning(traceback.format_exc())
        return default

    def __setitem__(self, key, value):
        if pd and np and isinstance(value, (np.ndarray, np.generic)):
            value = pd.DataFrame({json.dumps(list(value.shape)): value.reshape([-1])})
            key_with_suffix = ".".join([key, "np"])
        elif pd and isinstance(value, pd.Series):
            value = pd.DataFrame({"data": value})
            key_with_suffix = ".".join([key, "sr"])
        elif pd and isinstance(value, pd.DataFrame):
            key_with_suffix = ".".join([key, "df"])
        else:
            key_with_suffix = ".".join([key, "o"])
        if key in self.keys():
            del self[key]
        if pd and isinstance(value, pd.DataFrame):
            value.columns = value.columns.astype("string")
            value.to_parquet(self.root / ".".join([key_with_suffix, "parquet", "dc"]))
        else:
            pickle.dump(value, (self.root / ".".join([key_with_suffix, "pkl", "dc"])).open("wb"))

    def __delitem__(self, key):
        self._map()[key].unlink()

    def clear(self):
        [self.__delitem__(key) for key in self.keys()]

    def items(self):
        for key in self.keys():
            yield key, self.__getitem__(key)

    def values(self):
        for key in self.keys():
            yield self.__getitem__(key)


class DataCenters:
    def __init__(self, root: Union[pathlib.Path, str]):
        self.root = pathlib.Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.name = self.root.name

    def _map(self):
        return {file.name: DataCenter(file) for file in self.root.glob("*") if file.is_dir()}

    def keys(self):
        return self._map().keys()

    def __getitem__(self, key):
        return self._map()[key]

    def get(self, key: str, *_):
        try:
            return self.__getitem__(key)
        except Exception:
            (self.root / key).mkdir(parents=True, exist_ok=True)
            return self.__getitem__(key)

    def __delitem__(self, key):
        self._map()[key].rmdir()

    def clear(self):
        [self.__delitem__(key) for key in self.keys()]

    def items(self):
        return self._map().items()

    def values(self):
        return self._map().values()
