import datetime

from prompt_toolkit import HTML
from prompt_toolkit.application import get_app
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.formatted_text import fragment_list_width, to_formatted_text, merge_formatted_text
from prompt_toolkit.styles import Style

tool_name = "InstaGram"
tool_version = "v2.1.0"
tool_title = f"{tool_name} - {tool_version}"

run_msg = "Run the attack?"
run_msg_prefix = "[y/n]: "

proxies = {}
proxy_controlPort = 9051
protocols = ["socks5", "socks", "http", "https", "ftp", "ssh"]
proxy_options = {"ControlPort": proxy_controlPort}

update_controlPort = lambda port: proxy_options.update({"ControlPort": port})

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
        "tool": "bg:#%s #222222" % (fg,),
        "target": "bg:#%s bold" % (fg,),
        "password": "bg:#0043d1 bold",
        "all-passwords": "bg:#009dd1 bold",
        "percentage": "bg:#D18E00 bold",
        "done-with": "bg:#ACD100 bold",
        "time": "bg:#%s #222222" % (fg,),
        "sep": "bg:#000000",
        "true": "bg:#04FF00 bold",
        "false": "bg:#FF0000 bold",
        # "analyzed": "bg:#B0B0B0",
        "arg1": "#09C406 bold",
        "arg2": "#06C1C4",
        "arg3": "#B0B0B0",
        "query-username": "purple",
        "trailing-input": "#ff1500 bold",  # wrong input color foreground
        "label": "bg:#B0B0B0",
        "value": "bg:#B0B0B0 bold",
        "left-part": "bg:#%s #%s" % (bg, bg),
        "right-part": "bg:#%s #%s" % (bg, bg),
        "padding": "bg:#%s #%s" % (bg, bg),
    }
)

done_passwords = 0
total_passwords = 0
progress = "0.00%"
current_password = "-"

passwords = []
retry_passwords = []
wls = {}  # wls=wordlists
execution_history = []
analyzed = False
options = {"target": "", "sound": "", "delay": 3, "timeout": 15, "rest": 5, "log": True}  # , "threads": 3}
update_options = lambda key, value: options.update({key: value})
path_completer = PathCompleter(expanduser=True, only_directories=False)

completer = {
    "target": None,
    "wordlist": {
        "list": None,
        "count": wls,
        "analyze": wls,
        "add": path_completer,
        "remove": wls
    },
    # pattern:
    # socks5:127.0.0.1:5000 <Password>
    # proxy add socks5:127.0.0.1:5000 w3b9086w30698hy3wht
    "proxy": {
        "list": None,
        "import": path_completer,
        "identity": {"new": proxies, "check": proxies},
        "control_port": None,
        "options": None,
        "protocols": None,
        "add": None,
        "remove": proxies,
    },
    "options": {
        "show": None,
        "set": {
            "log": {"true": None, "false": None},  # 3
            "rest": None,  # 5 (rest per minutes when over requesting)
            "sound": path_completer,  # alarm-siren.wav (will be played if password found!!)
            "delay": None,  # 3
            "timeout": None,  # 15
        }
    },
    "bruteforce": {
        "run": None
    },
    "set": {
        "title": None,
    },
    "password": {
        "list": None,  # show all
        "count": None,  # show number
        "query": None,  # check if password is in list
        "place": {},  # get place of password in passwords list
        "sort": {"ascending": None, "descending": None, "shuffle": None},
        "add": None,  # add manually
        "retry": None,  # non-tried passwords
        "remove": {},  # remove manually
        "clear": None  # clear all passwords list
    },
    "status": None,
    "history": {"clear": None, "save": None},
    "help": None,
    "clear": None,
    "exit": None
}


def Corrections():
    return {
        # 10
        "targ": "target",
        "targe": "target",
        "targte": "target",
        "targtt": "target",
        "targee": "target",
        "targr": "target",
        "targrt": "target",
        "targe6": "target",
        "taret": "target",
        "taget": "target",

        # 24
        "histoy": "history",
        "hitory": "history",
        "histoyy": "history",
        "histryy": "history",
        "hisrry": "history",
        "hostry": "history",
        "histor": "history",
        "histry": "history",
        "histoyr": "history",
        "hisotr": "history",
        "jistory": "history",
        "gistory": "history",
        "hostory": "history",
        "hustory": "history",
        "hidtory": "history",
        "hiatory": "history",
        "hisyory": "history",
        "hisrory": "history",
        "histpry": "history",
        "histiry": "history",
        "histoty": "history",
        "histoey": "history",
        "historu": "history",
        "histort": "history",

        # 11
        "sho": "show",
        "shw": "show",
        "shlw": "show",
        "dhow": "show",
        "ahow": "show",
        "sjow": "show",
        "sgow": "show",
        "shpw": "show",
        "shiw": "show",
        "shoe": "show",
        "shoq": "show",

        # 13
        "clea": "clear",
        "claer": "clear",
        "cler": "clear",
        "vlear": "clear",
        "xlear": "clear",
        "c;ear": "clear",
        "ckear": "clear",
        "clrar": "clear",
        "clwar": "clear",
        "cledr": "clear",
        "clesr": "clear",
        "cleat": "clear",
        "cleae": "clear",

    }


def Bottom_Toolbar():
    # analyzed = f"<true>{self.wordlists_analyzed}</true>" if self.wordlists_analyzed == True else f"<false>{self.wordlists_analyzed}</false>"
    left_part = HTML(
        "<left-part>"
        f" <tool> {tool_name} </tool> <sep>|</sep>"
        f" <label>Target:</label> <target>{options['target']}</target> <sep>|</sep>"
        f" <label>Passwords:</label> <all-passwords>{len(passwords)}</all-passwords> <sep>|</sep>"
        f" <label>Attempts:</label> <all-passwords>{done_passwords}</all-passwords> <sep>|</sep>"
        f" <label>Progress:</label> <percentage>{progress}</percentage> <sep>|</sep>"
        f" <label>Proxy:</label> <all-passwords>{len(proxies)}</all-passwords> <sep>|</sep>"
        "</left-part>"
    )
    right_part = HTML(
        "<right-part> "
        " <time> %s </time> "
        "</right-part>"
    ) % (datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S"),)

    used_width = sum(
        [
            fragment_list_width(to_formatted_text(left_part)),
            fragment_list_width(to_formatted_text(right_part)),
        ]
    )

    total_width = get_app().output.get_size().columns
    padding_size = total_width - used_width

    padding = HTML("<padding>%s</padding>") % (" " * padding_size)

    return merge_formatted_text([left_part, padding, right_part])
