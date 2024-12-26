import json
import argparse
import os
import panel as pn
from panels import load_frequency, load_frequency_comparison, load_lift_progress, load_weight_lifted

pn.extension(design="native", sizing_mode="stretch_width")

@pn.cache
def load_data(args):
    if not os.path.exists(args.input):
        print(f'File {args.input} does not exist.')
        return
    
    with open(args.input, 'r') as f:
        data = json.load(f)
    return data

def main():
    # Parse the input arguments
    parser = argparse.ArgumentParser(description='A tool to viualize workout data.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Path to the input data file.')
    args = parser.parse_args()

    # Load the data
    data = load_data(args)
    if not data:
        return
    
    # Get the unique exercises
    exercises = set()
    for item in data:
        for key in item['exercises'].keys():
            exercises.add(key)
    exercises = sorted(exercises)
    exercises.append('All')

    # Define the input widgets
    time_interval_select = pn.widgets.Select(name='Time Interval', options=['week', 'month', 'year'], value='month')
    exercise_select = pn.widgets.Select(name='Exercise', options=exercises, value='All')
    
    # Load the components
    frequency = load_frequency(data, time_interval_select, exercise_select)
    weight_lifted = load_weight_lifted(data, time_interval_select, exercise_select)
    lift_progress = load_lift_progress(data, exercise_select)
    frequency_comparison = load_frequency_comparison(data, exercise_select)

    # Create the main layout
    pn.template.MaterialTemplate(title="GymMetrics", main=[
        pn.Row(time_interval_select, exercise_select),
        frequency,
        weight_lifted,
        lift_progress,
        frequency_comparison
    ]).servable()

main()