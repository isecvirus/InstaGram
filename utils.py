import itertools

from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.shortcuts import yes_no_dialog, input_dialog
from prompt_toolkit.styles import Style

ig_rainbow = lambda text:''.join([f"<style color='{color}'>{c2}</style>" for color,c2 in zip(itertools.cycle(["#405DE6", "#833AB4", "#C13584", "#E1306C", "#FD1D1D", "#F56040", "#F77737", "#FCAF45", "#FFDC80"]), [c1 for c1 in text])])

def YesNo(message: str, title: str = "InstaGram", yes: str = "yes", no: str = "no"):
    style = Style.from_dict({
        'dialog': 'bg:#88ff88',
        'dialog frame.label': 'bg:#ffffff #000000',
        'dialog.body': 'bg:#000000 #00ff00',
        'dialog shadow': 'bg:#00aa00',
    })
    dialog = yes_no_dialog(yes_text=yes, no_text=no, text=message, title=title, style=style).run(in_thread=True)
    return dialog


def Input(message: str, title: str = "InstaGram",
          completer: NestedCompleter = NestedCompleter.from_nested_dict({}), cancel_text: str = "Cancel",
          ok_text: str = "OK", password: bool = False, default: str = ""):
    style = Style.from_dict({
        'dialog': 'bg:#88ff88',
        'dialog frame.label': 'bg:#ffffff #000000',
        'dialog.body': 'bg:#000000 #00ff00',
        'dialog shadow': 'bg:#00aa00',
    })
    return input_dialog(title=title, text=message, completer=completer, cancel_text=cancel_text, ok_text=ok_text,
                        password=password, default=default, style=style).run()



def percentage(p: int, a: int) -> str:
    return "{:.2f}%".format((p * 100 / a)) # part, all
