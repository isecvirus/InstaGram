from prompt_toolkit.contrib.regular_languages.lexer import GrammarLexer
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.contrib.regular_languages.compiler import compile
from vars import completer


def Lexer():
    def command_validation():
        return compile(
            f"\s*((?P<arg1>({'|'.join(list(completer.keys()))})) \s+ (?P<arg2>(\S+)) \s+ (?P<arg3>(\S+)))\s*"
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