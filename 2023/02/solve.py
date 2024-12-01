#!/usr/bin/env python
import pathlib

DATA_FILE = pathlib.Path(__file__).parent / "data.txt"
with DATA_FILE.open() as fd:
  data = fd.readlines()
  
