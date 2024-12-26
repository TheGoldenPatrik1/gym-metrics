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

def plot_exercise_frequency_comparison(data, sort_by_frequency, hide_low_values, low_values_threshold, exercise):
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
        lambda x: 'red' if x == exercise else '#0072b5'
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

def load_frequency_comparison(data, exercise_select):
    def build_content():
        sort_by_frequency = pn.widgets.Checkbox(name='Sort by Frequency', value=True)
        low_values_checkbox = pn.widgets.Checkbox(name='Hide Values Under', value=True, width=120, align=('start', 'center'))
        low_values_input = pn.widgets.IntInput(name='', value=5, step=1, start=0, end=100, width=50, align='start')
        low_values = pn.Row(low_values_checkbox, low_values_input)

        def update_exercise_frequency_comparison(sort_by_frequency, hide_low_values, low_values_threshold, exercise):
            return plot_exercise_frequency_comparison(data, sort_by_frequency, hide_low_values, low_values_threshold, exercise)
        exercise_frequency_comparison = pn.bind(
            update_exercise_frequency_comparison, sort_by_frequency, low_values_checkbox, low_values_input, exercise_select
        )

        return [sort_by_frequency, low_values, exercise_frequency_comparison]
    
    return lazy_load_accordion('Exercise Frequency Comparison', build_content)