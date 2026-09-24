#!/usr/bin/env python3
"""Acquire/aggregate Putnam P08 from NCCS harmonized historical BMF snapshots.
Downloads one selected snapshot per observed year, filters 501(c)(3), counts
unique EIN by 50 states. No interpolation; snapshot month is always retained.
Large raw BMF files are not committed to GitHub by this script.
"""
from pathlib import Path
import hashlib,json,requests
import pandas as pd

# Prefer a mid/late-year vintage when available; only catalog-verified vintages.
VINTAGES={
2000:"2000_05",2001:"2001_07",2002:"2002_07",2003:"2003_07",
2004:"2004_12",2005:"2005_07",2006:"2006_01",
2009:"2009_07",2010:"2010_07",2011:"2011_07",2012:"2012_07",
2013:"2013_07",2014:"2014_04",2015:"2015_12",2016:"2016_08",
2018:"2018_12",2019:"2019_08",2020:"2020_04",2022:"2022_08",
2023:"2023_06"}
# Catalog-confirmed harmonized/transformed snapshots only.
# No harmonized monthly release is listed for 2007, 2008, 2017, 2021.
# Raw-archive-only 2017 releases are NOT silently mixed into the harmonized series.
