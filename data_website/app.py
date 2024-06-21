

import pandas as pd
import prepprocess
import barchart

# Load the CSV file into a DataFrame
DF_Data = pd.read_csv(r'C:\Users\samir\Desktop\Data Visualization\project\project_data.csv')

# Process the data
final_results = prepprocess.DataProcessing(DF_Data)
win_loss_record = prepprocess.CalculateWinsLosses(final_results)

# Generate the chart
italic_country_names = barchart.MakeItalic(win_loss_record)
fig = barchart.DrawBarChart(italic_country_names, win_loss_record)

# Optionally, show the figure
fig.show()