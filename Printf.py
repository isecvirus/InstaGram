from os import get_terminal_size
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style

def printf(data:str, mt:str="msg", **kwargs):
    try:
        # mt=message type
        message_types = {"msg": "#696969", "warn": "#afb553", "error": "#b55353", "info": "#53b4b5", "success": "#53b558"}

        if mt in message_types:
            color = message_types[mt]
        else:
            color = message_types["msg"]

        style = Style.from_dict({
            "data": "bg:%s #222222" %color,
            "padding": "bg:%s" %color
        })

        data = " " + str(data) + " "
        width = get_terminal_size().columns - len(data)
        print_formatted_text(HTML(f"<data>{data}</data><padding>{' ' * width}</padding>"), style=style, **kwargs)
    except Exception:
        """
        when formatting error occurres just print out the given data.
        """
        print_formatted_text(str(data))