#############################################################################
#  CHAP_average_replica_plots.py -- A python script to calculate and plot   #
#    average of replica plots from MD trajectory analysis                   #
#  CHAP_average_replica_plots.py is part of CHAPERONg                       #
#  Input parameters are generated by GROMACS and read by this script        #
#  CHAPERONg -- An automation program for GROMACS MD simulations and        #
#    trajectory analyses                                                    #
#############################################################################

__author__  = 'Abeeb A. Yekeen'
__email__   = 'abeeb.yekeen@hotmail.com'
__date__    = '2023.06.22'
__version__ = '1.0'
__status__  = 'Production'


import os
import sys
import time
import argparse
import numpy as np

# Create an argument parser
parser = argparse.ArgumentParser(description="Generate averaged plots and stats for multiple .xvg data")
parser.add_argument("-d", "--directory",
                    help="Path to the directory containing the input xvg files")
parser.add_argument("-l", "--label",
                    help="Name/Type of the input files, e.g. RMSD, Rg, SASA, etc.")
args = parser.parse_args()

# Get label and path to the input files
input_directory = args.directory or os.getcwd()
label = args.label or "Data"

# Check if the input directory exists
if not os.path.isdir(input_directory):
    print("\nInvalid input directory path.")
    sys.exit(1)

# Make a list of input files in the directory
input_files = [file for file in os.listdir(input_directory) if file.endswith(".xvg")]
file_count = len(input_files)

# Load data from input files
print("\n Loading data from input files found in the working directoy...\n")
time.sleep(1)
data = []
for file_name in input_files:
    file_path = os.path.join(input_directory, file_name)
    with open(file_path, "r") as file:
        lines = file.readlines()
        # Grab the labels for x and y axes from the input files
        for line in lines:
            if ("xaxis" in line and "label" in line):
                xlabel = line
                xtitle_split = line.split('"')
                xtitle = xtitle_split[1].strip()
                if "(" in xtitle: xtitle_no_unit = (xtitle.split("("))[0].strip()
                elif " " in xtitle: xtitle_no_unit = (xtitle.split())[0].strip()
                else: xtitle_no_unit = xtitle
            if ("yaxis" in line and "label" in line):
                ylabel = line
                ytitle_split = line.split('"')
                ytitle = ytitle_split[1].strip()
                if "(" in ytitle: ytitle_no_unit = (ytitle.split("("))[0].strip()
                elif " " in ytitle: ytitle_no_unit = (ytitle.split())[0].strip()
                else: ytitle_no_unit = ytitle
            if "@TYPE" in line:
                plot_type = line
        plot_title = f'@    title "Averaged {label}"\n'
        plot_legend = f'@ s0 legend "Mean of {file_count} replica plots"\n'
        # Skip header lines and comments
        lines = [line for line in lines if not (line.startswith("#") or line.startswith("@"))]
        # Extract x and y values
        x = []
        y = []
        for line in lines:
            values = line.strip().split()
            x.append(float(values[0]))
            y.append(float(values[1]))
        data.append((file_name, y))  # Store file name along with y values

# Calculate mean and standard deviation
print(" Calculating mean and standard deviation...\n")
time.sleep(1)
mean_data = np.mean([y for _, y in data], axis=0)
std_data = np.std([y for _, y in data], axis=0)

# Generate new xvg file with averaged data
print(f" Generating the {xtitle_no_unit}-averaged {ytitle_no_unit} plot...\n")
time.sleep(1)
output_file_mean = os.path.join(input_directory, f"mean_{label}.xvg")
with open(output_file_mean, "w") as file:
    file.write(f"# Mean {ytitle_no_unit}\n")
    file.write(f"{plot_title}{xlabel}{ylabel}{plot_type}{plot_legend}")
    for i in range(len(x)):
        file.write(f"{x[i]}\t{mean_data[i]:.8f}\n")

# Generate new file with x-axis, y-axis, and std dev
print(f" Writing out the {xtitle_no_unit}-averaged {xtitle_no_unit}-stddev lookup file...\n")
time.sleep(1)
output_file_stats = os.path.join(input_directory, f"mean_{label}_stats.dat")
with open(output_file_stats, "w") as file:
    file.write(f"{xtitle_no_unit}\tMean\tStd-dev\n")
    for i in range(len(x)):
        file.write(f"{x[i]}\t{mean_data[i]:.8f}\t{std_data[i]:.8f}\n")

# Generate new file with x-axis, y-axis, mean, and std dev
print(f" Writing out the {xtitle_no_unit}-{ytitle_no_unit}_values-averaged {ytitle_no_unit}-stddev lookup file...\n")
time.sleep(1)
output_file_data = os.path.join(input_directory, f"{label}_input_replicas.dat")
with open(output_file_data, "w") as file:
    file.write(f"{xtitle_no_unit}\t")
    file.write("\t".join([file_name.rstrip(".xvg") for file_name, _ in data]))
    file.write("\tMean\tStd-dev\n")
    for i in range(len(x)):
        file.write(f"{x[i]}\t")
        file.write("\t\t".join([str(y[i]) for _, y in data]))  # Write y-axis values
        file.write(f"\t\t{mean_data[i]:.8f}\t\t{std_data[i]:.8f}\n")  # Write mean and std dev values

print(" Run successfully completed!!!\n")
