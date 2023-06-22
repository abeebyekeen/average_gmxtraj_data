import os
import numpy as np
import time

# Get the current working directory containing input files
input_directory = os.getcwd()

# Make a list of input files in the directory
input_files = [file for file in os.listdir(input_directory) if file.endswith(".xvg")]

# Load data from input files
print("\n Loading data from input files found in the working directoy...\n")
time.sleep(1)
data = []
for file_name in input_files:
    file_path = os.path.join(input_directory, file_name)
    with open(file_path, "r") as file:
        lines = file.readlines()
        # Fetch the labels for x and y axes
        for line in lines:
            if ("xaxis" in line and "label" in line):
                xlabel = line
            if ("yaxis" in line and "label" in line):
                ylabel = line
            if "@TYPE" in line:
                plot_type = line
        plot_title = '@    title "Averaged Data"\n'
        plot_legend = '@ s0 legend "Average"\n'
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

# Calculate mean and dtd-dev
print(" Calculating mean and standard deviation...\n")
time.sleep(1)
mean_data = np.mean([y for _, y in data], axis=0)
std_data = np.std([y for _, y in data], axis=0)

# Generate new xvg file with averaged data
print(" Writing out the time-average plot...\n")
time.sleep(1)
output_file_mean = "mean_data.xvg"
with open(output_file_mean, "w") as file:
    file.write("# Mean Data\n")
    file.write(f"{plot_title}{xlabel}{ylabel}{plot_type}{plot_legend}")
    for i in range(len(x)):
        file.write(f"{x[i]}\t{mean_data[i]:.8f}\n")

# Generate new file with time, data, and std dev
print(" Writing out the time-average-stddev lookup file...\n")
time.sleep(1)
output_file_stats = "data_stats.dat"
with open(output_file_stats, "w") as file:
    file.write("Time\tMean\tStd-dev\n")
    for i in range(len(x)):
        file.write(f"{x[i]}\t{mean_data[i]:.8f}\t{std_data[i]:.8f}\n")

# Generate new file with time, y-axis values, mean, and std dev
print(" Writing out the time-data_values-average-stddev lookup file...\n")
time.sleep(1)
output_file_data = "data_values.dat"
with open(output_file_data, "w") as file:
    file.write("Time\t")
    file.write("\t".join([file_name.rstrip(".xvg") for file_name, _ in data]))
    file.write("\tMean\tStd-dev\n")
    for i in range(len(x)):
        file.write(f"{x[i]}\t")
        file.write("\t\t".join([str(y[i]) for _, y in data]))  # Write y-axis values
        file.write(f"\t\t{mean_data[i]:.8f}\t\t{std_data[i]:.8f}\n")  # Write mean and std dev values

print(" Run successfully completed!!!\n")
