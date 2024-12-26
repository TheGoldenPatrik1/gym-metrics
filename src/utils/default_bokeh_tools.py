from bokeh.models import WheelZoomTool

wheel_zoom = WheelZoomTool(zoom_on_axis=False)
default_bokeh_tools = ['pan', wheel_zoom]