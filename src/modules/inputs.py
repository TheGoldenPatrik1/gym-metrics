import panel as pn
import utils

def load_inputs(settings, data):
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

    # Initialize the callbacks
    init_callbacks(inputs, settings, data)

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
    inputs['exercise_select'][visible - 1].value = 'Unselected'
    if visible == 5:
        inputs['plus_icon'].disabled = False
    if visible == 3:
        inputs['minus_icon'].disabled = True

def build_exercise_select(i):
    initial_value = 'All' if i == 0 else 'Unselected'
    return pn.widgets.Select(
        name=f'Exercise {i+1}',
        groups={
            'Splits': [],
            'Groups': [],
            'Muscles': [],
            'Exercises': [],
            'Default': [initial_value]
        },
        value=initial_value,
        visible=i < 2
    )

def init_callbacks(inputs, settings, data):
    exercises = utils.load_exercises(data)
    splits, groups, muscles = utils.load_classes(data)

    def build_select_list(dict):
        keys = sorted(dict.keys())
        return [
            item for item in keys if not settings['low_values_checkbox'].value or dict[item] > settings['low_values_input'].value
        ]
    
    def update_exercise_select(i):
        options = inputs['exercise_select'][i].groups
        options['Splits'] = build_select_list(splits)
        options['Groups'] = build_select_list(groups)
        options['Muscles'] = build_select_list(muscles)
        options['Exercises'] = build_select_list(exercises)

    def load_exercise_select(i):
        settings['low_values_checkbox'].param.watch(update_exercise_select, 'value')
        settings['low_values_input'].param.watch(update_exercise_select, 'value')
        update_exercise_select(i)

    for i in range(len(inputs['exercise_select'])):
        load_exercise_select(i)

def display_inputs(inputs):
    return pn.Row(
        inputs['time_interval_select'],
        *inputs['exercise_select'],
        inputs['plus_icon'],
        inputs['minus_icon'],
        inputs['settings_icon']
    )