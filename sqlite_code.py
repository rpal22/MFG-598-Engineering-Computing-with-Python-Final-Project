import sqlite3
from range import ParameterRange


def alert_if_out_of_range(value: float, value_name: str, param_range: ParameterRange):
    if value < param_range.minimum:
        print(f'{value_name} value {value} is below minimum ({param_range.minimum})')
    elif value > param_range.maximum:
        print(f'{value_name} value {value} is above maximum ({param_range.maximum})')


range_amb_humid = ParameterRange('AmbientConditions.AmbientHumidity.U.Actual', 13.85, 17.25)
range_amb_temp = ParameterRange('AmbientConditions.AmbientTemperature.U.Actual', 23.03, 24.42)

con = sqlite3.connect('mfg_data.db')
cur = con.cursor()

sql_query = """select
    "AmbientConditions.AmbientHumidity.U.Actual", 
    "AmbientConditions.AmbientTemperature.U.Actual"
from prod_data
"""

for row in cur.execute(sql_query):
    amb_humid, amb_temp = row
    alert_if_out_of_range(amb_humid, 'Ambient Humidity', range_amb_humid)
    alert_if_out_of_range(amb_temp, 'Ambient Temperature', range_amb_temp)

con.close()


