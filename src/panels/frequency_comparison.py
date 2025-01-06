import panel as pn
import pandas as pd
import plotly.express as px
from components import lazy_load_accordion
import utils

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
    
    # Color the columns of selected exercises
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
    ).opts(default_tools=utils.default_bokeh_tools)

def collect_pie_data(data, exercise, cls):
    # Collect the frequency of each exercise in a given class
    pie_data = {}
    for item in data:
        for key in item['exercises'].keys():
            classes = utils.get_exercise_classes(key)
            if classes[cls] != None and exercise in classes[cls]:
                if key not in pie_data:
                    pie_data[key] = 0
                pie_data[key] += 1
    return pie_data

def plot_group_frequency_single(data, exercise, cls, hide_low_values, low_values_threshold):
    # Collect the data
    pie_data = collect_pie_data(data, exercise, cls)
    if hide_low_values:
        for key in list(pie_data.keys()):
            if pie_data[key] < low_values_threshold:
                if 'Other' not in pie_data:
                    pie_data['Other'] = 0
                pie_data['Other'] += pie_data[key]
                del pie_data[key]

    # Plot the data
    df_data = {
        'Exercise': pie_data.keys(),
        'Frequency': pie_data.values()
    }
    df = pd.DataFrame(df_data)
    return px.pie(df, values='Frequency', names='Exercise', title=f'{exercise} Exercise Breakdown')

def plot_group_frequency_comparison(data, hide_low_values, low_values_threshold, exercises):
    plots = []
    for exercise in exercises:
        cls = utils.get_class(exercise)
        if cls != 'exercise':
            plots.append(plot_group_frequency_single(data, exercise, cls, hide_low_values, low_values_threshold))
    return pn.Column(*plots)

def load_frequency_comparison(data, inputs, settings):
    exercise_select = inputs['exercise_select']
    low_values_checkbox = settings['low_values_checkbox']
    low_values_input = settings['low_values_input']

    def build_content():
        sort_by_frequency = pn.widgets.Checkbox(name='Sort by Frequency', value=True)

        def update_exercise_frequency_comparison(sort_by_frequency, hide_low_values, low_values_threshold, *exercises):
            return plot_exercise_frequency_comparison(data, sort_by_frequency, hide_low_values, low_values_threshold, exercises)
        exercise_frequency_comparison = pn.bind(
            update_exercise_frequency_comparison, sort_by_frequency, low_values_checkbox, low_values_input, *exercise_select
        )

        def update_group_frequency_comparison(hide_low_values, low_values_threshold, *exercises):
            return plot_group_frequency_comparison(data, hide_low_values, low_values_threshold, exercises)
        group_frequency_comparison = pn.bind(
            update_group_frequency_comparison, low_values_checkbox, low_values_input, *exercise_select
        )

        return [sort_by_frequency, exercise_frequency_comparison, group_frequency_comparison]
    
    return lazy_load_accordion('Exercise Frequency Comparison', build_content)