import json
import argparse
import os
import panel as pn
import panels
import modules

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
    settings = modules.load_settings_inputs()
    inputs = modules.load_inputs()

    # Define callbacks to update the input widgets
    for i in range(len(inputs['exercise_select'])):
        def update_exercise_select():
            inputs['exercise_select'][i].options = [
                exercise for exercise in exercise_names if not settings['low_values_checkbox'].value or exercise == 'All' or exercises[exercise] > settings['low_values_input'].value
            ]
            if i > 0:
                inputs['exercise_select'][i].options[len(inputs['exercise_select'][i].options) - 1] = 'Unselected'
        settings['low_values_checkbox'].param.watch(update_exercise_select, 'value')
        settings['low_values_input'].param.watch(update_exercise_select, 'value')
        update_exercise_select()
    
    # Load the components
    frequency = panels.load_frequency(data, inputs['time_interval_select'], inputs['exercise_select'])
    weight_lifted = panels.load_weight_lifted(data, inputs['time_interval_select'], inputs['exercise_select'])
    lift_progress = panels.load_lift_progress(data, inputs['exercise_select'])
    frequency_comparison = panels.load_frequency_comparison(data, inputs['exercise_select'], settings['low_values_checkbox'], settings['low_values_input'])

    # Create the main layout
    template = pn.template.MaterialTemplate(title="GymMetrics", main=[
        modules.display_inputs(inputs),
        frequency,
        weight_lifted,
        lift_progress,
        frequency_comparison
    ])

    # Build the settings modal
    inputs['settings_icon'].on_click(lambda _: template.open_modal())
    modal = modules.load_settings_modal(settings)
    template.modal.append(modal)
    
    # Serve the app
    template.servable()

main()