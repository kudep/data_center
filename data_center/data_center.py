from typing import Union, Any

import pathlib
import pickle
import logging

import traceback

logger = logging.getLogger(__name__)

try:
    import pandas as pd
except Exception:
    pd = False


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
        type = file.suffixes[0]
        if type == ".parquet":
            return pd.read_parquet(file)
        elif type == ".pkl":
            return pickle.load(file.open("rb"))
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
        if pd and isinstance(value, pd.DataFrame):
            value.columns = value.columns.astype("string")
            value.to_parquet(self.root / ".".join([key, "parquet", "dc"]))
        else:
            pickle.dump(value, (self.root / ".".join([key, "pkl", "dc"])).open("wb"))

    def __delitem__(self, key):
        self._map()[key].unlink()

    def items(self):
        for key in self.keys():
            yield key, self.__getitem__(key)


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

    def items(self):
        for key in self.keys():
            yield key, self.__getitem__(key)
