from subprocess import run
from os import listdir
from re import match
from time import strftime

STATE = "IL"
DATA_NAME = "LAI" # "et"
FILENAME_REGEX = "^\d{7}\.nc$" if DATA_NAME == "et" else "^LAI\d{7}\.nc$"

INPUT_PATH, OUTPUT_PATH = ".", "."
IN_DAWN_SERVER = True

if IN_DAWN_SERVER:
  if DATA_NAME == "et":
    INPUT_PATH = "/mnt/gfs01/DAWN-ML/et_data_nc"
    OUTPUT_PATH = f"/mnt/gfs01/DAWN-ML/et_data_nc_{STATE}"
  elif DATA_NAME == "LAI":
    INPUT_PATH=  "/mnt/gfs01/DAWN-ML/MODIS_LAI_4DAWN_GeoTiff"
    OUTPUT_PATH=  f"/mnt/gfs01/DAWN-ML/LAI_data_nc_{STATE}"

arg0 = "cdo"
arg1 = "sellonlatbox,-91.51,-87.52,36.98,42.49"

"""
this program will take all of the entire mainland US ET data in .nc format and
crop out just Illinois (or whatever state you choose)

it runs the following CDO command as a process, and CDO takes care of cropping
the data and putting the output wherever we specify.

% cdo sellonlatbox,-91.51,-87.52,36.98,42.49 infile.nc outfile.nc

you'll have to specify the coordinates, these 4 are specific to Illinois
"""


### now onto the algo ###


filenames = listdir(INPUT_PATH)
count = 0

for filename in filenames:

  # ensure we're running cdo on the correct .nc file
  if not match(FILENAME_REGEX, filename):
    continue
  
  # good file, so run cdo on it; ALSO if you want to display the output of every file processed (it's a lot) set capture_output=False
  cmd_output = run([arg0, arg1, f"{INPUT_PATH}/{filename}", f"{OUTPUT_PATH}/{STATE}_{filename}"], shell=False, capture_output=True)

  # ensure that it ran successfully
  if cmd_output.returncode != 0:
    print(f"error with cdo:\n{cmd_output}")
  else:
    count += 1
  
  # print output to give feedback that the program is running
  if count % 365 == 0:
    print(f"{strftime('%X')} : processed {count//365} year(s) of data")
  
print(f"done. processed {count} files in total")