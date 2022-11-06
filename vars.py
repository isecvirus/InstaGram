from prompt_toolkit.styles import Style

bg = "444444"
fg = "dddddd"
style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#CF0000",
        "completion-menu.completion.current": "bg:#FF3838",
        "completion-menu.meta.completion.current": "bg:#FF3838",
        "scrollbar.background": "bg:#FF0000",
        "scrollbar.button": "bg:#870000",
        "scrollbar.arrow": "bg:#870000",
        "real-bg": "bg:#%s" % bg,
        "tool": "bg:#%s #222222" % (fg, ),
        "target": "bg:#%s bold" % (fg, ),
        "password": "bg:#0043d1 bold",
        "all-passwords": "bg:#009dd1 bold",
        "percentage": "bg:#D18E00 bold",
        "done-with": "bg:#ACD100 bold",
        "time": "bg:#%s #222222" % (fg, ),
        "sep": "bg:#000000",
        "true": "bg:#04FF00 bold",
        "false": "bg:#FF0000 bold",
        # "analyzed": "bg:#B0B0B0",
        "arg1": "#09C406 bold",
        "arg2": "#06C1C4",
        "arg3": "#B0B0B0",
        "query-username": "purple",
        "trailing-input": "#ff1500 bold", # wrong input color foreground
        "label": "bg:#B0B0B0",
        "value": "bg:#B0B0B0 bold",
        "left-part": "bg:#%s #%s" % (bg, bg),
        "right-part": "bg:#%s #%s" % (bg, bg),
        "padding": "bg:#%s #%s" % (bg, bg),
    }
)