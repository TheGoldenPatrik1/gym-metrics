import panel as pn

def lazy_load_accordion(name, build_content):
    loading_spinner = pn.indicators.LoadingSpinner(value=True, size=40, name='Loading...')
    content = pn.Column(loading_spinner)

    def update_accordion(event):
        if len(event.new) == 0:
            content[:] = [loading_spinner]
        else:
            content[:] = build_content()
    
    accordion = pn.Accordion((name, content))
    accordion.param.watch(update_accordion, "active")

    return accordion