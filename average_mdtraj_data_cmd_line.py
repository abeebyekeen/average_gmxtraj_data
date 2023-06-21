import os
import sys
import argparse
import numpy as np

# Create an argument parser
parser = argparse.ArgumentParser(description="Generate averaged plots and stats for multiple .xvg data")
parser.add_argument("-d", "--directory",
                    help="Path to the directory containing the input xvg files")
parser.add_argument("-l", "--label",
                    help="String label")
args = parser.parse_args()

# Get label and path to the input files
input_directory = args.directory or os.getcwd()
label = args.label or ""

# Check if the input directory exists
if not os.path.isdir(input_directory):
    print("\nInvalid input directory path.")
    sys.exit(1)

# Make a list of input files in the directory
input_files = [file for file in os.listdir(input_directory) if file.endswith(".xvg")]

# Load data from input files
data = []
for file_name in input_files:
    file_path = os.path.join(input_directory, file_name)
    with open(file_path, "r") as file:
        lines = file.readlines()
        # Skip the header lines
        lines = [line for line in lines if not line.startswith("#")]
        # Extract x and y values
        x = []
        y = []
        for line in lines:
            values = line.strip().split()
            x.append(float(values[0]))
            y.append(float(values[1]))
        data.append((file_name, y))  # Store file name along with y values

# Calculate mean and standard deviation
mean_rmsd = np.mean([y for _, y in data], axis=0)
std_rmsd = np.std([y for _, y in data], axis=0)

# Generate new xvg file with mean rmsd
output_file_mean = os.path.join(input_directory, f"{label}_mean_rmsd.xvg")
with open(output_file_mean, "w") as file:
    file.write("# Mean RMSD\n")
    for i in range(len(x)):
        file.write(f"{x[i]} {mean_rmsd[i]:.7f}\n")  # Write mean rmsd values with 7 decimal places

# Generate new file with time, rmsd, and standard deviation
output_file_stats = os.path.join(input_directory, f"{label}_rmsd_stats.txt")
with open(output_file_stats, "w") as file:
    file.write("Time\tRMSD\tStandard Deviation\n")
    for i in range(len(x)):
        file.write(f"{x[i]}\t{mean_rmsd[i]:.7f}\t{std_rmsd[i]:.7f}\n")  # Write mean and standard deviation values with 7 decimal places

# Generate new file with time, y-axis values, mean, and standard deviation
output_file_data = os.path.join(input_directory, f"{label}_data_values.txt")
with open(output_file_data, "w") as file:
    file.write("Time\t")
    file.write("\t".join([file_name for file_name, _ in data]))  # Write column headers
    file.write("\tMean\tStandard Deviation\n")  # Additional column headers
    for i in range(len(x)):
        file.write(f"{x[i]}\t")
        file.write("\t".join([str(y[i]) for _, y in data]))  # Write y-axis values
        file.write(f"\t{mean_rmsd[i]:.7f}\t{std_rmsd[i]:.7f}\n")
