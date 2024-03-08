from settings import settings
from menus import GreetingScreen, MainMenu
from util import close

def main():
    if settings.getValue("firstLaunch") == str(True):
        GreetingScreen.run()

    MainMenu.run()
    close(0)

if __name__ == "__main__":
    main()
