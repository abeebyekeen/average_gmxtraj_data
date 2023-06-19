import numpy as np

# List of input file names
input_files = ["A.xvg", "B.xvg", "C.xvg"]

# Load data from input files
data = []
for file_name in input_files:
    with open(file_name, "r") as file:
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
        data.append(y)

# Calculate mean and standard deviation
mean_rmsd = np.mean(data, axis=0)
std_rmsd = np.std(data, axis=0)

# Generate new xvg file with mean rmsd
output_file_mean = "mean_rmsd.xvg"
with open(output_file_mean, "w") as file:
    file.write("# Mean RMSD\n")
    for i in range(len(x)):
        file.write(f"{x[i]} {mean_rmsd[i]}\n")

# Generate new file with time, rmsd, and standard deviation
output_file_stats = "rmsd_stats.txt"
with open(output_file_stats, "w") as file:
    file.write("Time\tRMSD\tStandard Deviation\n")
    for i in range(len(x)):
        file.write(f"{x[i]}\t{mean_rmsd[i]}\t{std_rmsd[i]}\n")

print("Files generated successfully.")
