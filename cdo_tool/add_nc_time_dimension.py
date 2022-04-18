from os import listdir, system
from time import strftime
# from re import match
# import xarray as xr

"""
takes .nc files and adds a time dimension to them,
then concats them all together into one file

currently meant for ET and LAI data for Matthew's
project.
"""

STATE, DATA_NAME = "IL", "LAI" # "et"
FILENAME_REGEX = "^\d{7}\.nc$" if DATA_NAME == "et" else "^LAI\d{7}\.nc$"

INPUT_PATH, OUTPUT_PATH, ROOT = ".", ".", "/mnt/gfs01/DAWN-ML"
IN_DAWN_SERVER = True

if IN_DAWN_SERVER:
  INPUT_PATH  = f"{ROOT}/{DATA_NAME}_data_nc_{STATE}"
  OUTPUT_PATH = f"{ROOT}/{DATA_NAME}_data_nc_{STATE}"


""" my method """


# get all filenames sorted
# filenames = sorted([f for f in listdir(INPUT_PATH) if match(FILENAME_REGEX, f)])

# # concat them all together along a new time dimension, the times are just integers here, then save it
# state_datasets = [xr.open_dataset(f"{INPUT_PATH}/{d}") for d in filenames]
# concatted = xr.concat(objs=state_datasets, dim='time')
# concatted.to_netcdf(path="{OUTPUT_PATH}/{DATA_NAME}_all_{STATE}.nc", mode="w")

# print(f"created file at {OUTPUT_PATH}/{DATA_NAME}_all_{STATE}.nc")


""" Matthew's method """


OUT_ROOT = "/home/zsating"
OUT_NAME = f"{DATA_NAME}_all_{STATE}.nc"
OUTFILE = f"{OUT_ROOT}/{OUT_NAME}"

system(f"ncecat -u time {INPUT_PATH}/*.nc {OUTFILE}") 
system(f"ncap2 -O -s 'time[time]=array(7296,1,$time)' {OUTFILE} {OUTFILE}")
system(f"ncatted -O -a units,time,o,c,\"days since 2001-01-01\" {OUTFILE}")
system(f"ncatted -O -h -a history,global,o,c,'N/A' {OUTFILE}")