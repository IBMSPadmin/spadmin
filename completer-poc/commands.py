import sys, inspect

class SpadminCommand:

    def short_help(self) -> str:
        return 'Short description of command'

    def help(self) -> str:
        return """Detailed description of command
        with many lines
        """

    def _execute(self, parameters: str) -> str:
        return "not defined: " + parameters

    def execute(self, paramter):
        print(self._execute(paramter))


class cmd_1(SpadminCommand):
    def short_help(self) -> str:
        return 'ez az elso parancsom'

    def help(self) -> dict:
        return """az elso parancsom csak kiir egy szot
        ennyi.
        """

    def _execute(self, parameters: str) -> str:
        return "parameter: " + parameters


class cmd_2(SpadminCommand):
    def short_help(self) -> str:
        return 'ez az elso parancsom'

    def help(self) -> dict:
        return """az elso parancsom csak kiir egy szot
        ennyi.
        """



cmd = cmd_1()
cmd.execute("aaaa")
print("--------------")
cmd2 = cmd_2()
cmd2.execute("aaaa")

print("--------------")
print(cmd.help())
print(cmd.short_help())

print("--------------")

for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj):
        print(obj.__name__)
