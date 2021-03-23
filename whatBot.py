from os.path import dirname, basename, isfile, join
import sys
import glob
import importlib

# cut name of bot from sys
modules = glob.glob(join(dirname(__file__), "bot", "*.py"))
# store the name of bot
modules = ["bot." + i.rsplit("\\", 2)[-1].split('.')[0] for i in modules]

callBot = None
print("-----BOT-----")
for i, k in enumerate(modules):
    print(f"{i + 1}. {k.split('.')[1]}")
while callBot is None:
    try:
        choice = int(input("> "))
        importlib.import_module(modules[choice - 1])
        callBot = sys.modules[modules[choice - 1]].callBot
        break
    except:
        print("Unable to import bot")
        pass
