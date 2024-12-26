import panel as pn
import pandas as pd
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models import HoverTool
from components import lazy_load_accordion, stat_table
from utils import default_bokeh_tools

def multiply_sets_reps_weight(data):
    sets = data['sets'] if 'sets' in data else 1
    reps = data['reps'] if 'reps' in data else 1
    return sets * reps * data['weight']

def calculate_exercise_weight_lifted(exercise_data):
    total = 0
    if isinstance(exercise_data, list):
        for data in exercise_data:
            total += multiply_sets_reps_weight(data)
    elif '1RM' in exercise_data:
        total += exercise_data['1RM']
    else:
        total += multiply_sets_reps_weight(exercise_data)
    return total

def build_df(data, exercise):
    df = []

    # Loop through the data and extract the weight lifted
    for item in data:
        for key in item['exercises'].keys():
            if exercise == 'All' or exercise == key:
                exercise_data = item['exercises'][key]
                if type(exercise_data) is bool or type(exercise_data) is str:
                    continue
                total_weight_lifted = calculate_exercise_weight_lifted(exercise_data)
                df.append({
                    'date': item['date'],
                    'exercise': key,
                    'weight_lifted': total_weight_lifted
                })
    
    # Create a DataFrame from the data
    df = pd.DataFrame(df)
    if df.empty:
        df = pd.DataFrame(columns=['date', 'weight_lifted'])
    return df

def get_weight_lifted_df(data, time_interval, exercise):
    df = build_df(data, exercise)

    if df['weight_lifted'].sum() == 0:
        return df, df

    df['date'] = pd.to_datetime(df['date'])

    if time_interval == 'week':
        # Group by week
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['week'] = df['date'].dt.isocalendar().week
        weight_lifted = df.groupby(['year', 'week'])['weight_lifted'].sum().reset_index()

        # Create a full range of 'year-week' combinations and merge with the grouped data
        date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='W-MON')  # Weekly start
        date_range_df = pd.DataFrame({'year': date_range.year, 'week': date_range.isocalendar().week})
        weight_lifted = pd.merge(date_range_df, weight_lifted, on=['year', 'week'], how='left', validate="many_to_many")
        weight_lifted['weight_lifted'] = weight_lifted['weight_lifted'].fillna(0)
        weight_lifted['weight_lifted'] = weight_lifted['weight_lifted'].astype(int)

        # Format df
        weight_lifted['date'] = weight_lifted.apply(
            lambda row: pd.Timestamp.fromisocalendar(row['year'], row['week'], 1), axis=1
        )
        weight_lifted = weight_lifted[['date', 'weight_lifted']]
    elif time_interval == 'month':
        # Group by month
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        weight_lifted = df.groupby(['year', 'month'])['weight_lifted'].sum().reset_index()
        
        # Create a full range of 'year-month' combinations and merge with the grouped data
        date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='MS')  # Monthly start
        date_range_df = pd.DataFrame({'year': date_range.year, 'month': date_range.month})
        weight_lifted = pd.merge(date_range_df, weight_lifted, on=['year', 'month'], how='left', validate="many_to_many")
        weight_lifted['weight_lifted'] = weight_lifted['weight_lifted'].fillna(0)

        # Format df
        weight_lifted['date'] = pd.to_datetime(weight_lifted[['year', 'month']].assign(day=1))
        weight_lifted['date'] =  weight_lifted['date'].dt.strftime('%B %Y')
        weight_lifted = weight_lifted[['date', 'weight_lifted']]
    elif time_interval == 'year':
        # Group by year
        df['date'] = df['date'].dt.year
        weight_lifted = df.groupby('date')['weight_lifted'].sum().reset_index()

    return df, weight_lifted

def generate_weight_lifted_stats(data, time_interval, exercise):
    _, weight_lifted = get_weight_lifted_df(data, time_interval, exercise)
    return stat_table(weight_lifted, 'weight_lifted')

def plot_weight_lifted(data, time_interval, exercise):
    _, weight_lifted = get_weight_lifted_df(data, time_interval, exercise)

    hover = HoverTool(
        tooltips=[("date", "@date{%F}" if time_interval == "week" else "@date"), ("weight_lifted", "@weight_lifted{0,0}")],
        formatters={"@date": "datetime"}
    )
    plot = weight_lifted.hvplot.bar(
        x='date',
        y='weight_lifted',
        width=800,
        height=400,
        rot=90,
        yformatter=NumeralTickFormatter(format='0,0'),
        ylabel='Weight Lifted (lbs)',
        xlabel='Date'
    ).opts(tools=[hover], default_tools=default_bokeh_tools)

    return plot

def load_weight_lifted(data, time_interval_select, exercise_select):
    def build_content():
        def update_weight_lifted_stats(time_interval, exercise):
            return generate_weight_lifted_stats(data, time_interval, exercise)
        weight_lifted_stats = pn.bind(update_weight_lifted_stats, time_interval=time_interval_select, exercise=exercise_select)
        def update_weight_lifted_plot(time_interval, exercise):
            return plot_weight_lifted(data, time_interval, exercise)
        weight_lifted_plot = pn.bind(update_weight_lifted_plot, time_interval=time_interval_select, exercise=exercise_select)
        return [weight_lifted_stats, weight_lifted_plot]
    
    weight_lifted_header = pn.bind(
        lambda time_interval, exercise: f'{"" if exercise == "All" else exercise + " "}Weight Lifted per {time_interval.capitalize()}',
        time_interval=time_interval_select,
        exercise=exercise_select
    )
    
    return lazy_load_accordion(weight_lifted_header, build_content)