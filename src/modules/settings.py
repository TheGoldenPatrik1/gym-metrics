import panel as pn

def load_settings_inputs():
    inputs = {}

    inputs['low_values_checkbox'] = pn.widgets.Checkbox(name='Hide Values Under', value=True, width=130, align=('start', 'center'))
    inputs['low_values_input'] = pn.widgets.IntInput(name='', value=5, step=1, start=0, end=100, width=50, align='start')

    return inputs

def load_settings_modal(settings):
    low_values = pn.Row(settings['low_values_checkbox'], settings['low_values_input'])
    modal = pn.Column('## Settings', low_values, width=500)

    return modal