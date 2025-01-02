import panel as pn
import pandas as pd
from components import lazy_load_accordion
from utils import default_bokeh_tools

def build_df(data):
    # Get the frequency of each exercise
    exercises = {}
    for item in data:
        for key in item['exercises'].keys():
            if key not in exercises:
                exercises[key] = 0
            exercises[key] += 1
    df = pd.DataFrame(list(exercises.items()), columns=['Exercise', 'Frequency'])
    return df

def plot_exercise_frequency_comparison(data, sort_by_frequency, hide_low_values, low_values_threshold, exercises):
    # Build the DataFrame
    df = build_df(data)

    # Filter the data based on the checkboxes
    if hide_low_values:
        df = df[df['Frequency'] >= low_values_threshold]
    if sort_by_frequency:
        df = df.sort_values(by='Frequency', ascending=True)
    else:
        df = df.sort_values(by='Exercise')
    
    df['Color'] = df['Exercise'].apply(
        lambda x: 'red' if x in exercises else '#0072b5'
    )

    # Plot the data
    return df.hvplot.bar(
        x='Exercise',
        y='Frequency',
        color='Color',
        width=800,
        height=400,
        rot=90,
        hover_tooltips=[('Exercise', '@Exercise'), ('Frequency', '@Frequency')]
    ).opts(default_tools=default_bokeh_tools)

def load_frequency_comparison(data, exercise_select, low_values_checkbox, low_values_input):
    def build_content():
        sort_by_frequency = pn.widgets.Checkbox(name='Sort by Frequency', value=True)

        def update_exercise_frequency_comparison(sort_by_frequency, hide_low_values, low_values_threshold, *exercises):
            return plot_exercise_frequency_comparison(data, sort_by_frequency, hide_low_values, low_values_threshold, exercises)
        exercise_frequency_comparison = pn.bind(
            update_exercise_frequency_comparison, sort_by_frequency, low_values_checkbox, low_values_input, *exercise_select
        )

        return [sort_by_frequency, exercise_frequency_comparison]
    
    return lazy_load_accordion('Exercise Frequency Comparison', build_content)