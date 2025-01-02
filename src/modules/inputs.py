import panel as pn

def load_inputs():
    inputs = {}

    # Define the input widgets
    inputs['time_interval_select'] = pn.widgets.Select(name='Time Interval', options=['week', 'month', 'year'], value='month')
    inputs['exercise_select'] = [build_exercise_select(i) for i in range(5)]
    inputs['plus_icon'] = pn.widgets.Button(
        name="",
        button_type="primary",
        icon="plus",
        width=40,
        align="end",
        on_click=lambda _: plus_icon_click(inputs)
    )
    inputs['minus_icon'] = pn.widgets.Button(
        name="",
        button_type="primary",
        icon="minus",
        width=40,
        align="end",
        disabled=True,
        on_click=lambda _: minus_icon_click(inputs)
    )
    inputs['settings_icon'] = pn.widgets.Button(
        name="",
        button_type="primary",
        icon="settings",
        width=50,
        align="end"
    )

    return inputs

def plus_icon_click(inputs):
    visible = 0
    for input in inputs['exercise_select']:
        if input.visible:
            visible += 1
        else:
            break
    inputs['exercise_select'][visible].visible = True
    if visible == 4:
        inputs['plus_icon'].disabled = True
    if visible == 2:
        inputs['minus_icon'].disabled = False

def minus_icon_click(inputs):
    visible = 0
    for input in inputs['exercise_select']:
        if input.visible:
            visible += 1
    inputs['exercise_select'][visible - 1].visible = False
    if visible == 5:
        inputs['plus_icon'].disabled = False
    if visible == 3:
        inputs['minus_icon'].disabled = True

def build_exercise_select(i):
    initial_value = 'All' if i == 0 else 'Unselected'
    return pn.widgets.Select(
        name=f'Exercise {i+1}',
        options=[initial_value],
        value=initial_value,
        visible=i < 2
    )

def display_inputs(inputs):
    return pn.Row(
        inputs['time_interval_select'],
        *inputs['exercise_select'],
        inputs['plus_icon'],
        inputs['minus_icon'],
        inputs['settings_icon']
    )