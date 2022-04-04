# import xarray as xr
# import pandas as pd
# import numpy as np
# from netCDF4 import Dataset
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import subprocess

output = subprocess.run(["cdo", "sellonlatbox,-91.51,-87.52,36.98,42.49", "2020365.nc", "IL_2020365.nc"])

paths = []