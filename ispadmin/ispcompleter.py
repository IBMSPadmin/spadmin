from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
import random
from prompt_toolkit.completion import Completer, Completion

query = NestedCompleter.from_nested_dict({
    'node': None,
    'session': None,
    'process': None,
})


def getnodes():
    print("called")
    return {random.choice("gfdghiuztzgvhbnja"), random.choice("gfdghiuztzgvhbnja"), "node1", "node2", "node3"}


update = {
    'node': getnodes(),
    'stgpool': None,
    'devclass': None,
}

completer = {

    'show': {
        'version': None,
        'clock': None,
        'ip': {
            'interface': {'brief'}
        }
    },
    'query': query,
    'update': update,
    'exit': None,
}


class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
            print("itt", document)
            av = Completion("aaaa", start_position=0)
            yield av
            yield Completion('completion2', start_position=0)
            yield Completion('completion3', start_position=0)
            print (document.cursor_position)


# text = prompt('# ', completer=completer)
text = prompt('> ', completer=MyCustomCompleter())

print('You said: %s' % text)
