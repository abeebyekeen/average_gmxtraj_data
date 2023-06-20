import os
import numpy as np
import time

# Get the current working directory containing input files
input_directory = os.getcwd()

# Make a list of input files in the directory
input_files = [file for file in os.listdir(input_directory) if file.endswith(".xvg")]

# Load data from input files
print("Loading data from the input files found in the working directoy...\n")
time.sleep(1)
data = []
for file_name in input_files:
    file_path = os.path.join(input_directory, file_name)
    with open(file_path, "r") as file:
        lines = file.readlines()
        # Skip the header lines
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
print("Calculating mean and standard deviation...\n")
time.sleep(1)
mean_data = np.mean([y for _, y in data], axis=0)
std_data = np.std([y for _, y in data], axis=0)

# Generate new xvg file with averaged data
print("Writing out the time-average plot...\n")
time.sleep(1)
output_file_mean = "mean_data.xvg"
with open(output_file_mean, "w") as file:
    file.write("# Mean Data\n")
    for i in range(len(x)):
        file.write(f"{x[i]} {mean_data[i]}\n")

# Generate new file with time, data, and std dev
print("Writing out the time-average-stddev lookup file...\n")
time.sleep(1)
output_file_stats = "data_stats.txt"
with open(output_file_stats, "w") as file:
    file.write("Time\Data\tStd-dev\n")
    for i in range(len(x)):
        file.write(f"{x[i]}\t{mean_data[i]}\t{std_data[i]}\n")

# Generate new file with time, y-axis values, mean, and std dev
print("Writing out the time-data_values-average-stddev lookup file...\n")
time.sleep(1)
output_file_data = "data_values.txt"
with open(output_file_data, "w") as file:
    file.write("Time\t")
    file.write("\t".join([file_name for file_name, _ in data]))
    file.write("\tMean\tStandard Deviation\n")
    for i in range(len(x)):
        file.write(f"{x[i]}\t")
        file.write("\t".join([str(y[i]) for _, y in data]))  # Write y-axis values
        file.write(f"\t{mean_data[i]}\t{std_data[i]}\n")  # Write mean and std dev values

print("Run successfully completed!!!")
