import pandas as pd
import panel as pn
from bokeh.models import HoverTool
from functools import reduce
from components import lazy_load_accordion
from utils import default_bokeh_tools
import constants

def build_sets_str(data):
    if 'sets' not in data or 'reps' not in data:
        return f"@ {data['weight']}"
    return f"{data['sets']}x{data['reps']} @ {data['weight']}"

def extract_weight_lifted(exercise_data):
    value = 0
    sets = []
    if isinstance(exercise_data, list):
        for data in exercise_data:
            sets.append(build_sets_str(data))
            if data['weight'] > value and data['reps'] > 3:
                value = data['weight']
        sets = ', '.join(sets)
    else:
        sets = build_sets_str(exercise_data)
        value = exercise_data['weight']
    return value, sets

def extract_item(dfs, item, exercise):
    if exercise in item['exercises']:
        exercise_data = item['exercises'][exercise]
        if type(exercise_data) is bool or type(exercise_data) is str:
            return
        if '1RM' in exercise_data:
            weight_lifted = exercise_data['1RM']
            sets = '1RM'
        else:
            weight_lifted, sets = extract_weight_lifted(exercise_data)
        obj = {
            'date': item['date'],
            'exercise': exercise,
            'weight_lifted': weight_lifted,
            'sets': sets
        }
        if '1RM' in sets:
            dfs['1rm'].append(obj)
        elif 'x7' in sets or 'x8' in sets or 'x10' in sets or 'x12' in sets or 'x' not in sets:
            dfs['low'].append(obj)
        elif 'x4' in sets or 'x5' in sets or 'x6' in sets:
            dfs['high'].append(obj)

def build_dfs(data, exercise):
    # Initialize the DataFrames
    dfs = {
        'low': [],
        'high': [],
        '1rm': []
    }

    # Loop through the data and extract the weight lifted
    for item in data:
        extract_item(dfs, item, exercise)
    
    # Create a DataFrame from the data
    for key in list(dfs.keys()):
        dfs[key] = pd.DataFrame(dfs[key])
        if dfs[key].empty:
            del dfs[key]
    return dfs

def build_all_dfs(data, exercises):
    dfs = {}
    for exercise in exercises:
        dfs[exercise] = build_dfs(data, exercise)
    return dfs

def calculate_lift_differences(data, exercises):
    dfs = build_all_dfs(data, exercises)
    df_count = sum([len(df) for df in dfs.values()])

    # Check if there are any differences
    if df_count == 0:
        return pn.pane.Markdown("There are no differences avaiable for the selected exercise(s).")

    # Calculate the differences
    differences = {}
    percentages = {}
    for exercise_key in dfs:
        for df_key in dfs[exercise_key]:
            if df_count > 5 and df_key == '1rm':
                continue
            diff = dfs[exercise_key][df_key]['weight_lifted'].iloc[0] - dfs[exercise_key][df_key]['weight_lifted'].iloc[-1]
            if diff == 0:
                continue
            weight_type = f" ({df_key})" if len(dfs[exercise_key]) > 1 else ""
            differences[f"{exercise_key}{weight_type}"] = diff
            percentages[f"{exercise_key}{weight_type}"] = diff / dfs[exercise_key][df_key]['weight_lifted'].iloc[0] * 100

    # Convert differences to a markdown table
    table = "| " + " | ".join(differences.keys()) + " |\n"
    table += "| " + " | ".join(["---" for _ in differences.keys()]) + " |\n"
    table += "| " + " | ".join([f"{differences[key]} ({percentages[key]:.2f}%)" for key in differences.keys()]) + " |"

    return pn.pane.Markdown(table)

def generate_label(num_exercises, num_weight_types, exercise, weight_type):
    if num_exercises == 1:
        if num_weight_types == 1:
            return None
        return weight_type
    if num_weight_types == 1:
        return exercise
    return f"{exercise} ({weight_type})"

def plot_lift_progress(data, exercises):
    dfs = build_all_dfs(data, exercises)
    df_count = sum([len(df) for df in dfs.values()])

    if df_count == 0:
        return pn.pane.Markdown("There is no data available for the selected exercise(s).")

    hover = HoverTool(
        tooltips=[("date", "@date{%F}"), ("weight lifted", "@weight_lifted"), ("sets", "@sets")],
        formatters={"@date": "datetime"}
    )

    plots = []

    for exercise_key in dfs:
        for df_key in dfs[exercise_key]:
            if df_count > 5 and df_key == '1rm':
                continue
            dfs[exercise_key][df_key]['date'] = pd.to_datetime(dfs[exercise_key][df_key]['date'])
            if df_key == '1rm':
                plot = dfs[exercise_key][df_key].hvplot.scatter(
                    x='date',
                    y='weight_lifted',
                    xlabel='Date',
                    ylabel='Weight Lifted',
                    height=400,
                    width=800,
                    size=8,
                    hover_cols=['sets'],
                    label=generate_label(len(dfs), len(dfs[exercise_key]), exercise_key, df_key)
                ).opts(tools=[hover])
            else:
                plot = dfs[exercise_key][df_key].hvplot.line(
                    x='date',
                    y='weight_lifted',
                    xlabel='Date',
                    ylabel='Weight Lifted',
                    height=400,
                    width=800,
                    line_width=3,
                    hover_cols=['sets'],
                    label=generate_label(len(dfs), len(dfs[exercise_key]), exercise_key, df_key)
                ).opts(tools=[hover])
            plots.append(plot)

    plot = reduce(lambda x, y: x * y, plots)
    if df_count > 1:
        plot = plot.opts(legend_position='top')
    plot = plot.opts(default_tools=default_bokeh_tools)

    return plot

def process_exercise_name(exercise):
    if exercise == 'Lower':
        return [constants.SQUAT, constants.DEADLIFT]
    if exercise == 'Upper':
        return [constants.PULLUPS, constants.OVERHEAD_PRESS, constants.BENCH]
    if exercise == 'Pull':
        return [constants.PULLUPS]
    if exercise == 'Push':
        return [constants.OVERHEAD_PRESS, constants.BENCH]
    return [exercise]

def generate_exercise_list(exercises):
    if exercises[0] == 'All':
        return [constants.PULLUPS, constants.OVERHEAD_PRESS, constants.BENCH, constants.SQUAT, constants.DEADLIFT]
    total_exercises = []
    for exercise in exercises:
        if exercise != 'Unselected':
            total_exercises.extend(process_exercise_name(exercise))
    total_exercises = list(dict.fromkeys(total_exercises))
    return total_exercises

def build_exercise_header(*exercises):
    if exercises[0] == 'All':
        return 'Lift Progress'
    exercises = [exercise for exercise in exercises if exercise != 'Unselected']
    if len(exercises) == 1:
        return f"{exercises[0]} Progress"
    return f"{' vs '.join(exercises)} Progress"

def load_lift_progress(data, inputs):
    exercise_select = inputs['exercise_select']

    def build_content():
        def update_lift_differences(*exercise_input):
            exercises = generate_exercise_list(exercise_input)
            return calculate_lift_differences(data, exercises)
        lift_differences = pn.bind(update_lift_differences, *exercise_select)

        def update_lift_progress_plot(*exercise_input):
            exercises = generate_exercise_list(exercise_input)
            return plot_lift_progress(data, exercises)
        lift_progress_plot = pn.bind(update_lift_progress_plot, *exercise_select)

        return [lift_differences, lift_progress_plot]

    lift_progress_header = pn.bind(build_exercise_header, *exercise_select)
    
    return lazy_load_accordion(lift_progress_header, build_content)