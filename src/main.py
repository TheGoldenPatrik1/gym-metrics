import json
import argparse
import os
import panel as pn
import panels
import modules

pn.extension(design="native", sizing_mode="stretch_width")
pn.extension('plotly')

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

    # Define the input widgets
    settings = modules.load_settings_inputs()
    inputs = modules.load_inputs(settings, data)
    
    # Load the components
    frequency = panels.load_frequency(data, inputs)
    weight_lifted = panels.load_weight_lifted(data, inputs)
    lift_progress = panels.load_lift_progress(data, inputs)
    frequency_comparison = panels.load_frequency_comparison(data, inputs, settings)

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