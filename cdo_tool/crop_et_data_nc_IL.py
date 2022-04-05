from sre_constants import IN
from subprocess import run
from os import listdir
from re import match
from time import strftime

INPUT_PATH, OUTPUT_PATH = "", ""
IN_DAWN_SERVER = False
if IN_DAWN_SERVER:
  INPUT_PATH = "/mnt/gfs01/DAWN-ML/et_data_nc"
  OUTPUT_PATH = "/mnt/gfs01/DAWN-ML/et_data_nc_IL"
else:
  INPUT_PATH = "./"
  OUTPUT_PATH = "./"

STATE = "IL"

arg0 = "cdo"
arg1 = "sellonlatbox,-91.51,-87.52,36.98,42.49"

"""
cmd is % cdo sellonlatbox,-91.51,-87.52,36.98,42.49 infile outfile
"""


### now onto the algo ###


filenames = listdir(INPUT_PATH)
count = 0

for filename in filenames:

  # ensure we're running cdo on the correct .nc file
  if not match("^\d{7}\.nc$", filename):
    continue
  
  # good file, so run cdo on it
  cmd_output = run([arg0, arg1, f"{INPUT_PATH}/{filename}", f"{OUTPUT_PATH}/{STATE}_{filename}"])

  # ensure that it ran successfully
  if cmd_output.returncode != 0:
    print(f"error with cdo:\n{cmd_output}")
  else:
    count += 1
  
  # print output to give feedback that the program is running
  if count % 365 == 0:
    print(f"{strftime('%X')} : processed {count//365} year(s) of data")
  
print(f"done. processed {count} files in total")