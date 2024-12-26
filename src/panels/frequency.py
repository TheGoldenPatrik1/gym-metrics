import holoviews as hv
import hvplot.pandas
import panel as pn
import pandas as pd
from components import lazy_load_accordion, stat_table
import holoviews as hv
from utils import default_bokeh_tools

def get_frequency_df(_data, time_interval, exercise):
    # Filter the data based on the selected exercise
    if exercise != 'All':
        data = []
        for item in _data:
            if exercise in item['exercises']:
                data.append({
                    'date': item['date'],
                    'exercise': item['exercises'][exercise]
                })
    else:
        data = _data

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

def generate_frequency_stats(data, time_interval, exercise):
    _, frequency = get_frequency_df(data, time_interval, exercise)
    return stat_table(frequency, 'count')

def plot_frequency(data, time_interval, exercise):
    # Get the frequency dataframe
    _, frequency = get_frequency_df(data, time_interval, exercise)
    average_count = frequency['count'].mean()

    # Plot the frequency based on the selected interval
    plot = frequency.hvplot.line(
        x='date',
        y='count',
        width=800,
        height=400,
        xlabel='Date',
        ylabel='Count'
    )
    avg_line = hv.HLine(average_count).opts(
        color='red',
        line_dash='dashed',
        line_width=2
    )
    plot = (plot * avg_line).opts(xrotation=90, default_tools=default_bokeh_tools)
    return plot

def load_frequency(data, time_interval_select, exercise_select):
    def build_content():
        def update_frequency_stats(time_interval, exercise):
            return generate_frequency_stats(data, time_interval, exercise)
        frequency_stats = pn.bind(update_frequency_stats, time_interval=time_interval_select, exercise=exercise_select)
        def update_frequency_plot(time_interval, exercise):
            return plot_frequency(data, time_interval, exercise)
        frequency_plot = pn.bind(update_frequency_plot, time_interval=time_interval_select, exercise=exercise_select)

        return [frequency_stats, frequency_plot]
    
    frequency_header = pn.bind(
        lambda time_interval, exercise: f'{"Workout" if exercise == "All" else exercise} Frequency per {time_interval.capitalize()}',
        time_interval=time_interval_select,
        exercise=exercise_select
    )

    return lazy_load_accordion(frequency_header, build_content)