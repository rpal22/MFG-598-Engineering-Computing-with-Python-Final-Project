import pandas as pd
import matplotlib.pyplot as plt


# Class to define the range of acceptable values for a given parameter
class ParameterRange:

    def __init__(self, param_name: str, minimum: float, maximum: float):
        self.param_name = param_name
        self.minimum = minimum
        self.maximum = maximum

    def __repr__(self):
        return f'parameter: {self.param_name}, min: {self.minimum}, max: {self.maximum}'
    

# List of parameter names to monitor
columns = [
    'AmbientConditions.AmbientHumidity.U.Actual',
    'AmbientConditions.AmbientTemperature.U.Actual',
    'Machine1.MotorAmperage.U.Actual',
    'Machine1.MotorRPM.C.Actual',
    'Machine1.MaterialPressure.U.Actual',
    'Machine1.MaterialTemperature.U.Actual',
    'Machine2.MotorAmperage.U.Actual',
    'Machine2.MotorRPM.C.Actual',
    'Machine2.MaterialPressure.U.Actual',
    'Machine2.MaterialTemperature.U.Actual',
    'Machine3.MotorAmperage.U.Actual',
    'Machine3.MotorRPM.C.Actual',
    'Machine3.MaterialPressure.U.Actual',
    'Machine3.MaterialTemperature.U.Actual',
    'Stage1.Output.Measurement0.U.Actual',
    'Stage1.Output.Measurement0.U.Setpoint',
    'Stage1.Output.Measurement1.U.Actual',
    'Stage1.Output.Measurement1.U.Setpoint',
    'Stage1.Output.Measurement2.U.Actual',
    'Stage1.Output.Measurement2.U.Setpoint'
]


# Function to create alerts and plots for out-of-range values
def alert_and_plot(df, param_range, values_file):

    # Inner function to print and log values that are out of range
    def print_oor_values(row, param_name, param_min, param_max):
        value = row[param_name]
        if value < param_range.minimum:
            print(f'{param_name} value {value} is below minimum ({param_min})')
            values_file.write(f'{param_name},{row["time_stamp"]},{value}\n')
        elif value > param_range.maximum:
            print(f'{param_name} value {value} is above maximum ({param_max})')
            values_file.write(f'{param_name},{row["time_stamp"]},{value}\n')
        return row
    
    
    # Filtering and applying the print_oor_values function
    value_name = param_range.param_name
    oor_df = df.loc[:, ['time_stamp', value_name]]
    oor_df = oor_df[(oor_df[value_name] < param_range.minimum) | (oor_df[value_name] > param_range.maximum)]
    oor_df.apply(print_oor_values, args=(value_name, param_range.minimum, param_range.maximum), axis=1)

    # Plotting the out-of-range values
    x, y = oor_df['time_stamp'], oor_df[value_name]
    # print(type(x))
    if not y.empty:
        plt.figure()
        plt.title(f'Out Of Range Values for {value_name}')
        plt.scatter(x, y, label=value_name)
        plt.xticks(rotation=45)
        for x_val, y_val in zip(x, y):
            plt.annotate(str(y_val), xy=(x_val, y_val), size=10, rotation=45)
        plt.legend()
        plt.tight_layout()
    

# Reading data from a CSV file and preprocessing timestamps
df = pd.read_csv('continuous_factory_process_edited.csv')
df['time_stamp'] = df['time_stamp'].apply(lambda dt: dt.split(' ')[-1])

# Calculating means and standard deviations for each parameter
values_df = df.drop('time_stamp', axis=1)
means = values_df.mean()
std = values_df.std()
means_and_stds = pd.DataFrame([means.values, std.values], columns=values_df.columns)

# Creating ParameterRange objects for each parameter based on mean and standard deviation
param_ranges = []
for c in columns:
    mean, std = means_and_stds[c][0], means_and_stds[c][1]
    param_ranges.append(ParameterRange(c, mean - 3*std, mean + 3*std))

# Writing out-of-range values to a file and plotting them
with open('values.csv', 'w') as values_file:
    values_file.write('param_name,time_stamp,value\n')
    for p_range in param_ranges:
        alert_and_plot(df, p_range, values_file)
plt.show()
