from os import get_terminal_size
from rich import print
from rich.text import Text

def printf(data:str, mt:str="msg", **kwargs):
    try:
        # mt=message type
        message_types = {"msg": "#696969", "warn": "#ffb553", "error": "#f55353", "info": "#53bfb5", "success": "#53b558", "auth": "#800080"}

        if mt in message_types:
            color = message_types[mt]
        else:
            color = message_types["msg"]

        data = " " + str(data) + " "
        width = get_terminal_size().columns - len(data)
        print(f"[#222222 on {color}]{data}[/#222222 on {color}][#222222 on {color}]{' ' * width}[/#222222 on {color}]")
    except Exception:
        """
        when formatting error occurres just print out the given data.
        """
        print(str(data))