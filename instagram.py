#!/usr/bin/python3
import json
import os
import random
import re
import sys

import requests
import rich.progress
from prompt_toolkit import HTML, PromptSession, print_formatted_text as print
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import set_title, confirm
from requests import options
from rich.console import Console

from Login import start_bruteforce
from help import __help__
from Printf import printf
from Validator import validator
from analyze import analyzer
from clear import ClearScreen
from lexer import Lexer
from proxy import proxy
from table import table
from utils import ig_rainbow
from vars import style, tool_title, tool_name, proxies, protocols, completer, execution_history, wls, retry_passwords, \
    options, analyzed, \
    run_msg, Bottom_Toolbar, Corrections, passwords, proxy_options


class InstaGram:
    def __init__(self):
        self.total_passwords = 0
        set_title(tool_title)
        self.history = InMemoryHistory()
        self.bindings = KeyBindings()
        self.completer_obj = NestedCompleter.from_nested_dict(completer)
        self.passwords = passwords
        self.analyzed = analyzed

    def Go(self):
        @self.bindings.add(" ")
        def _(event):
            b = event.app.current_buffer
            w = b.document.get_word_before_cursor()

            if w is not None:
                if w in Corrections():
                    b.delete_before_cursor(count=len(w))
                    b.insert_text(Corrections()[w])

            b.insert_text(" ")

        while True:
            try:
                self.completer_obj = NestedCompleter.from_nested_dict(completer)
                psession = PromptSession(style=style,
                                         enable_system_prompt=True, enable_history_search=True, enable_suspend=True,
                                         search_ignore_case=True, complete_in_thread=True, complete_while_typing=True,
                                         completer=self.completer_obj, wrap_lines=False, multiline=False,
                                         clipboard=PyperclipClipboard(), vi_mode=False, refresh_interval=0.999,
                                         history=self.history, auto_suggest=AutoSuggestFromHistory(),
                                         key_bindings=self.bindings,
                                         mouse_support=False, bottom_toolbar=Bottom_Toolbar,
                                         include_default_pygments_style=True,
                                         lexer=Lexer())
                insta_reg = re.findall('\S+', psession.prompt(
                    HTML(ig_rainbow(tool_name + " ~$ "))))
                if options['log']: execution_history.append([' '.join(insta_reg)])
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
                        options['target'] = target
                        printf("Success: target set to '%s'." % target, mt="success")
                    else:
                        if options['target']:
                            printf(options['target'], mt="msg")
                        else:
                            printf("Warning: set target first.", mt="warn")
                elif insta_reg[0] == "set":
                    if insta_reg[1] == "title":
                        if len(insta_reg) > 2:
                            set_title(insta_reg[2])
                        else:
                            set_title(tool_title)
                elif insta_reg[0] == "exit":
                    sys.exit()
                elif insta_reg[0] == "clear":
                    ClearScreen()
                elif insta_reg[0] == "history":
                    if len(insta_reg) > 1:
                        if insta_reg[1] == "clear":
                            execution_history.clear()
                        elif insta_reg[1] == "save":
                            if len(execution_history) > 0:
                                filename = str(random.randint(1000000000, 9999999999)) + ".txt"
                                if len(insta_reg) > 2:
                                    filename = insta_reg[2]
                                with open(filename, "w") as h:
                                    h.write(table.make(execution_history, headers=["#", "command"]))
                                h.close()
                                printf("Success: Saved history to '%s'" % filename, mt="success")
                            else:
                                printf("Error: There is no data in the history to save.", mt="error")
                    else:
                        table.print(execution_history, headers=["#", "command"])
                elif insta_reg[0] == "wordlist":
                    if insta_reg[1] == "add":
                        wordlist = insta_reg[2]
                        if wordlist not in wls:
                            wordlist = os.path.expanduser(wordlist)
                            if os.path.exists(wordlist):
                                if os.path.isfile(wordlist):
                                    try:
                                        with open(wordlist, "r", errors="ignore") as aw:  # aw=analyze wordlist
                                            l = len(aw.readlines())
                                        wls[wordlist] = None  # must be None to avoid Assertion error
                                        printf("Success: '%s' added to wordlists list." % os.path.split(wordlist)[-1],
                                               mt="success")
                                        printf("Info: '%s' = %sl" % (os.path.split(wordlist)[-1], l), mt="info")
                                        aw.close()
                                        self.analyzed = False
                                    except Exception:
                                        printf("Error: '%s' couldn't be processed to pre-analyze." % wordlist,
                                               mt="error")
                                elif os.path.isdir(wordlist):
                                    if os.path.exists(wordlist):
                                        wordlists_inDir = os.listdir(wordlist)
                                        if len(wordlists_inDir) > 0:
                                            for wl in wordlists_inDir:
                                                fullpath = os.path.join(wordlist, wl)
                                                if fullpath not in wls:
                                                    if os.path.isfile(fullpath) and os.path.exists(fullpath):
                                                        try:
                                                            with open(fullpath, "r",
                                                                      errors="ignore") as aw:  # aw=analyze wordlist
                                                                l = len(aw.readlines())
                                                            wls[fullpath] = None
                                                            printf("Success: '%s' added to wordlists list." %
                                                                   os.path.split(fullpath)[-1], mt="success")
                                                            printf(
                                                                "Info: '%s' = %sl" % (os.path.split(fullpath)[-1], l),
                                                                mt="info")
                                                            aw.close()
                                                            self.analyzed = False
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
                        if wordlist in wls:
                            wls.pop(wordlist)
                            printf("Success: '%s' removed from wordlists list." % wordlist, mt="success")
                        else:
                            printf("Error: '%s' not in the list." % wordlist, mt="error")
                    elif insta_reg[1] == "list":
                        for w in wls:
                            printf(w, mt="msg")
                    elif insta_reg[1] == "count":
                        if insta_reg[2] in wls:
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
                        if len(wls) > 0:
                            if insta_reg[2:]:
                                for file in insta_reg[2:]:
                                    if file in wls:
                                        analyzer.passwords(file=file)
                                        self.analyzed = True
                                    else:
                                        printf("Error: '%s' not in wordlists list." % file, mt="error")
                            else:
                                for wl in wls:
                                    analyzer.passwords(file=wl)
                                    self.analyzed = True
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
                        print(len(self.passwords))
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
                            printf("Warning: '%s' already in self.passwords list." % insta_reg[2], mt="warn")
                    elif insta_reg[1] == "clear":
                        self.passwords.clear()
                    elif insta_reg[1] == "retry":
                        if len(retry_passwords) > 0:
                            print("\n".join(retry_passwords))
                        else:
                            printf("Error: there are not self.passwords in the self.passwords retry list", mt="error")
                    elif insta_reg[1] == "remove":
                        if insta_reg[2] in self.passwords:
                            self.passwords.remove(insta_reg[2])
                        else:
                            printf("Error: '%s' is not in self.passwords list." % insta_reg[2], mt="error")
                    # self.target = self.Input(completer=self.completer_obj, message="Who is the victim?:")
                elif insta_reg[0] == "proxy":
                    if insta_reg[1] == "list":
                        table.print(
                            data=[[i] + list(proxies[i].values()) for i in [p for p in proxies.keys()]],
                            headers=["#", "id", "protocol", "ip", "port", "password"])
                    elif insta_reg[1] == "identity":
                        if insta_reg[2] == "new":
                            id = insta_reg[3]
                            if id in proxies:
                                proxy.new(proxy_data=proxies[id], controlPort=proxy_options['ControlPort'])
                            else:
                                printf("Error: '%s' is not a valid proxy id." % id, mt="error")
                        elif insta_reg[2] == "check":
                            id = insta_reg[3]
                            if id in proxies:
                                proxy.get_identity(id=id, proxy_data=proxies[id])
                            else:
                                printf("Error: '%s' is not a valid proxy id." % id, mt="error")
                    elif insta_reg[1] == "control_port":
                        if validator.port(insta_reg[2]):
                            proxy_options['ControlPort'] = int(insta_reg[2])
                            printf("success: tor ControlPort set to '%s'" % insta_reg[2], mt="success")
                        else:
                            printf("Error: '%s' is not a valid port (valid: 0-65535)." % insta_reg[2], mt="error")
                    elif insta_reg[1] == "protocols":
                        for i, p in enumerate(sorted(protocols), start=1):
                            printf(f"{i}: {p}", mt="msg")
                    elif insta_reg[1] == "options":
                        print(json.dumps(proxy_options, indent=4))
                    elif insta_reg[1] == "import":
                        file = insta_reg[2]
                        if os.path.exists(file):
                            if os.path.isfile(file):
                                try:
                                    with rich.progress.open(file, "r") as import_file:
                                        proxies_file = import_file.readlines()
                                        for p in proxies_file:
                                            proxy.add(re.findall('\S+', p))
                                except Exception as error:
                                    printf("Error: error occurred while importing '%s'" % file, mt="error")
                                    printf("Reason: '%s'" % error, mt="msg")
                    elif insta_reg[1] == "add":
                        proxy.add(input=insta_reg[2:])
                    elif insta_reg[1] == "remove":
                        id = insta_reg[2]
                        if id in proxies.keys():
                            proxies.pop(id)
                            printf("Success: proxy with id '%s' removed." % id, mt="success")
                        else:
                            printf("Error: no proxy with id '%s'." % id, mt="error")

                elif insta_reg[0] == "options":
                    if insta_reg[1] == "show":
                        print(options)
                    elif insta_reg[1] == "set":
                        if len(insta_reg) > 3:
                            if insta_reg[2] in options:
                                option = insta_reg[2]
                                value = insta_reg[3]
                                if option in list(completer["options"]["set"].keys()):
                                    try:
                                        if value in ["true", "false"]:
                                            v = bool(eval(str(value).title()))
                                            options[option] = v
                                            printf("Success: '%s' updated to '%s'." % (option, v), mt="success")
                                            printf("Info: '%s' now is '%s'." % (option, v), mt="info")
                                        elif isinstance(int(value), type(options[option])) and int(value) >= 1:
                                            options[option] = int(value)
                                            printf("Success: '%s' updated to '%s'." % (option, int(value)), mt="success")
                                            printf("Info: '%s' now is '%s'." % (option, options[option]), mt="info")
                                        else:
                                            printf("Error: '%s' is not value for '%s'." % (value, option), mt="error")
                                    except Exception:
                                        printf("Error: '%s' is not value for '%s'." % (value, option), mt="error")
                            else:
                                printf("Error: '%s' is not an options." % insta_reg[2], mt="error")
                        else:
                            printf("Error: '%s' value can't be empty" % insta_reg[2], mt="error")
                elif insta_reg[0] == "status":
                    data = {"is_analyzed": self.analyzed}  # , "attempts": self.done_passwords}
                    print(data)
                elif insta_reg[0] == "options":
                    data = {"target": options["target"], "wordlists": list(wls.keys())}
                    print(data)
                elif insta_reg[0] == "help":
                    printf(__help__)

                elif insta_reg[0] == "bruteforce":
                    if insta_reg[1] == "run":
                        if options['target']:
                            are_you_sure = confirm(run_msg, suffix=" [y/n]: ")
                            if are_you_sure:
                                start_bruteforce()
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
        completer['wordlist']['count'] = wls
        completer['wordlist']['analyze'] = wls
        completer['wordlist']['remove'] = wls

    def UpdateAfterAnalyze(self):
        completer['password']['place'] = {}.fromkeys(self.passwords, None)
        completer['password']['remove'] = {}.fromkeys(self.passwords, None)

    def UpdateAfterAddingProxy(self):
        completer['proxy']['identity']['new'] = {}.fromkeys(proxies, None)
        completer['proxy']['identity']['check'] = {}.fromkeys(proxies, None)
        completer['proxy']['remove'] = {}.fromkeys(proxies, None)

if __name__ == "__main__":
    ig = InstaGram()
    ig.Go()
