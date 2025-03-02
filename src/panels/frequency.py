import holoviews as hv
import hvplot.pandas
import panel as pn
import pandas as pd
from functools import reduce
from components import lazy_load_accordion, stat_table
import holoviews as hv
import utils

def extract_data_item(item, exercise_class, exercise):
    if exercise_class == 'exercise':
        if exercise in item['exercises']:
            return {
                'date': item['date'],
                'exercise': item['exercises'][exercise]
            }
    else:
        for key in item['exercises'].keys():
            classes = utils.get_exercise_classes(key)
            if classes[exercise_class] != None and exercise in classes[exercise_class]:
                return {
                    'date': item['date'],
                    'exercise': key
                }
    return None

def extract_data(_data, exercise):
    exercise_class = utils.get_class(exercise)
    if exercise == 'All':
        data = _data
    else:
        data = []
        for item in _data:
            item_data = extract_data_item(item, exercise_class, exercise)
            if item_data != None:
                data.append(item_data)
    return data

def get_frequency_df(_data, time_interval, exercise):
    # Filter the data based on the selected exercise
    data = extract_data(_data, exercise)

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Group by the selected time interval (week, month, or year)
    if time_interval == 'week':
        # Group by week
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['week'] = df['date'].dt.isocalendar().week
        frequency = df.groupby(['year', 'week']).size().reset_index(name='count')
        frequency['date'] = frequency.apply(
            lambda row: pd.Timestamp.fromisocalendar(row['year'], row['week'], 1), axis=1
        )
        frequency = frequency[['date', 'count']]
    elif time_interval == 'month':
        # Group by month
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        frequency = df.groupby(['year', 'month']).size().reset_index(name='count')

        frequency['date'] = pd.to_datetime(frequency[['year', 'month']].assign(day=1))
        frequency['date'] = frequency['date'].dt.strftime('%B %Y')
    elif time_interval == 'year':
        # Group by year
        df['date'] = df['date'].dt.year
        frequency = df.groupby('date').size().reset_index(name='count')

    return df, frequency

def generate_frequency_stats_single(data, time_interval, exercise, is_single):
    _, frequency = get_frequency_df(data, time_interval, exercise)
    return stat_table(frequency, 'count', False if is_single else exercise)

def generate_frequency_stats(data, time_interval, exercises):
    exercises = [exercise for exercise in exercises if exercise != 'Unselected']
    stats = [generate_frequency_stats_single(data, time_interval, exercise, len(exercises) == 1) for exercise in exercises]
    return pn.Column(*stats)

def plot_frequency_single(data, time_interval, exercise, is_single):
    # Get the frequency dataframe
    df, frequency = get_frequency_df(data, time_interval, exercise)
    average_count = frequency['count'].mean()

    # Plot the frequency based on the selected interval
    plot = frequency.hvplot.line(
        x='date',
        y='count',
        width=800,
        height=400,
        xlabel='Date',
        ylabel='Count',
        label=None if is_single else exercise
    )
    avg_line = hv.HLine(average_count).opts(
        line_dash='dashed',
        line_width=2
    )

    # Calculate the width of the dataframe
    width_of_df = (df['date'].max() - df['date'].min()).days

    return plot * avg_line, width_of_df

def plot_frequency(data, time_interval, exercises):
    exercises = [exercise for exercise in exercises if exercise != 'Unselected']
    is_single = len(exercises) == 1

    # Generate plots and sort by width of the DataFrame
    plots_with_widths = [plot_frequency_single(data, time_interval, exercise, is_single) for exercise in exercises]
    plots_with_widths.sort(key=lambda x: x[1], reverse=True)
    sorted_plots = [plot for plot, _ in plots_with_widths]

    # Combine plots
    plot = sorted_plots[0] if is_single else reduce(lambda x, y: x * y, sorted_plots)
    plot = plot.opts(xrotation=90, default_tools=utils.default_bokeh_tools)
    if not is_single:
        plot = plot.opts(legend_position='top')
    return plot

def build_frequency_header(time_interval, *exercises):
    workout_str = 'Workout' if exercises[0] == 'All' else exercises[0]
    exercises = [exercise for exercise in exercises if exercise != 'Unselected']
    if len(exercises) > 1:
        workout_str = ' vs '.join(exercises)
    return f'{workout_str} Frequency per {time_interval.capitalize()}'

def load_frequency(data, inputs):
    time_interval_select = inputs['time_interval_select']
    exercise_select = inputs['exercise_select']

    def build_content():
        def update_frequency_stats(time_interval, *exercises):
            return generate_frequency_stats(data, time_interval, exercises)
        frequency_stats = pn.bind(update_frequency_stats, time_interval_select, *exercise_select)
        
        def update_frequency_plot(time_interval, *exercises):
            return plot_frequency(data, time_interval, exercises)
        frequency_plot = pn.bind(update_frequency_plot, time_interval_select, *exercise_select)

        return [frequency_stats, frequency_plot]
    
    frequency_header = pn.bind(build_frequency_header, time_interval_select, *exercise_select)

    return lazy_load_accordion(frequency_header, build_content)