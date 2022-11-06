__help__ = {
    "@[USERNAME]": "Get instagram account information, Example: @secvirus",
    "target": ["<Target username> to set the little poor target (victim)", "Without <Target username> will output the <Target username>"],
    "wordlist": {
        "list": "List all added wordlists.",
        "count": "Get wordlist length",
        "analyze": ["<Wordlist file-name>", "Without <Wordlist file-name> will analyze all added <Wordlist file-name>"],
        "add": {
            "<directory>": "Will add all <files> in the <directory>",
            "<filename>": "Will add <filename>"
        },
        "remove": "Will remove <filename>"
    },
    "proxy": {
        "list": "List all added proxies",
        "import": "<filename> contains proxies pattern(<protocol>:<ip>:<port>)",
        "identity": {
            "new": "<id> of proxy to get new identity",
            "check": "<id> of proxy to get current identity"
        },
        "control_port": "<port> to set the proxy control <port>",
        "options": "To show the values of overall proxy options",
        "protocols": "List all available proxy protocols",
        "add": "Add new proxy pattern(<protocol>:<ip>:<port>)",
        "remove": "Remove proxy by <id>",
    },
    "options": {
        "show": "Show bruteforce options",
        "set": {
            # "threads": "Threads as a <number> of bruteforce (per proxy)",  # 3
            "rest": "Rest per <minutes> when over requesting",  # 3
            "sound": "<sound> to play when finding password", # alarm-siren.wav
            "delay": "Delay in <seconds> between every request", # 3
            "timeout": "Timeout in <seconds> for every request before it disconnect", # 15
        }
    },
    "bruteforce": {
        "run": "Let's rock and roll"
    },
    "set": {
        "title": "Set the terminal window <title>",
    },
    "password": {
        "list": "List all analyzed passwords",  # show all
        "count": "Get number of passwords",  # show number
        "query": "Check if <password> in the passwords list",  # check if password is in list
        "place": "Get the index/place of <password> in the passwords list",  # get place of password in passwords list
        "sort": {"ascending": "Sort passwords from a-z", "descending": "Sort passwords from z-a",
                 "shuffle": "Randomize passwords ordering (shake)"},
        "add": "Manually add <password>",  # add manually
        "retry": "Shows the passwords that couldn't be tried REASON(a lot of requests OR ip blocked & etc..), to try it again.",  # remove manually
        "remove": "Manually remove <password>",  # remove manually
        "clear": "Clear passwords list *ALL OF IT*"  # clear all passwords list
    },
    "status": "Show bruteforce status",
    "history": {"clear": "Clear session command execution history", "save": [
        "Save session command execution history (if not <file> parsed then random filename will be generated Ex:4673467347.txt)",
        "Save session command execution history to <file>"]},
    "help": "Show this help message",
    "clear": "Clear the screen",
    "exit": "Exit the tool *** UNSAVE WORK WILL NOT BE SAVED ***"
}
