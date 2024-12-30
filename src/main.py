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
    exercises = {}
    for item in data:
        for key in item['exercises'].keys():
            if key in exercises:
                exercises[key] += 1
            else:
                exercises[key] = 1
    exercise_names = sorted(exercises.keys())
    exercise_names.append('All')

    # Define the input widgets
    low_values_checkbox = pn.widgets.Checkbox(name='Hide Values Under', value=True, width=130, align=('start', 'center'))
    low_values_input = pn.widgets.IntInput(name='', value=5, step=1, start=0, end=100, width=50, align='start')
    time_interval_select = pn.widgets.Select(name='Time Interval', options=['week', 'month', 'year'], value='month')
    exercise_select = pn.widgets.Select(name='Exercise', options=['All'], value='All')
    settings_icon = pn.widgets.Button(
        name="",
        button_type="primary",
        icon="settings",
        width=50,
        align="end"
    )

    # Define callbacks to update the input widgets
    def update_exercise_select(_=None):
        exercise_select.options = [exercise for exercise in exercise_names if not low_values_checkbox.value or exercise == 'All' or exercises[exercise] > low_values_input.value]
    low_values_checkbox.param.watch(update_exercise_select, 'value')
    low_values_input.param.watch(update_exercise_select, 'value')
    update_exercise_select()
    
    # Load the components
    frequency = load_frequency(data, time_interval_select, exercise_select)
    weight_lifted = load_weight_lifted(data, time_interval_select, exercise_select)
    lift_progress = load_lift_progress(data, exercise_select)
    frequency_comparison = load_frequency_comparison(data, exercise_select, low_values_checkbox, low_values_input)

    # Create the main layout
    template = pn.template.MaterialTemplate(title="GymMetrics", main=[
        pn.Row(time_interval_select, exercise_select, settings_icon),
        frequency,
        weight_lifted,
        lift_progress,
        frequency_comparison
    ])

    # Build the settings modal
    settings_icon.on_click(lambda _: template.open_modal())
    low_values = pn.Row(low_values_checkbox, low_values_input)
    modal = pn.Column('## Settings', low_values, width=500)
    template.modal.append(modal)
    
    # Serve the app
    template.servable()

main()