import panel as pn

def load_inputs():
    inputs = {}

    # Define the input widgets
    inputs['time_interval_select'] = pn.widgets.Select(name='Time Interval', options=['week', 'month', 'year'], value='month')
    inputs['exercise_select'] = [
        pn.widgets.Select(name='Exercise', options=['All'], value='All'),
        pn.widgets.Select(name='Second Exercise', options=['Unselected'], value='Unselected')
    ]
    inputs['settings_icon'] = pn.widgets.Button(
        name="",
        button_type="primary",
        icon="settings",
        width=50,
        align="end"
    )

    return inputs

def display_inputs(inputs):
    return pn.Row(
        inputs['time_interval_select'],
        *inputs['exercise_select'],
        inputs['settings_icon']
    )