from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
import inspect


class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        if not document.text:
            yield Completion("accept", start_position=0)
            yield Completion("activate", start_position=0)
            yield Completion("assign", start_position=0)
            yield Completion("query", start_position=0)
            yield Completion("update", start_position=0)
            yield Completion("define", start_position=0)
            yield Completion("delete", start_position=0)
        elif document.text.startswith("a"):
            yield Completion("accept", start_position=0)
            yield Completion("activate", start_position=0)
            yield Completion("assign", start_position=0)
        elif document.text.startswith("a") or document.text.startswith("ac"):
            yield Completion("accept", start_position=0)
            yield Completion("activate", start_position=0)
        elif document.text.startswith("q") or document.text.startswith("qu") or document.text.startswith(
                "que") or document.text.startswith("quer"):
            yield Completion("query", start_position=0)
        elif document.text.startswith("query"):
            yield Completion("session", start_position=0)
            yield Completion("process", start_position=0)
        elif document.text.startswith("u") or document.text.startswith("up") or document.text.startswith(
                "upd") or document.text.startswith("upda") or document.text.startswith(
            "updat") or document.text.startswith("update"):
            yield Completion("stgpool", start_position=0)
            yield Completion('devclass', start_position=0)


print
text = prompt('> ', completer=MyCustomCompleter())

print('You said: %s' % text)
