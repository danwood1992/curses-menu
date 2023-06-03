import sys
from typing import Union
from django.core.management.base import BaseCommand, CommandParser
import curses

class Command(BaseCommand):
    help = 'Command with curses-based menu'

    def add_arguments(self, parser: CommandParser) -> None:
        pass

    def handle(self, *args: str, **options: Union[str, int]) -> None:
        curses.wrapper(self.menu)

    def menu(self, stdscr):
        current_option = 0
        options = [
            ("Setup", self.setup_submenu),
            ("Delete", self.delete_submenu),
            ("Tools", self.tools_submenu),
            ("Exit", sys.exit)
        ]

        # Initialize curses
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        stdscr.clear()
        # Hide the cursor
        curses.curs_set(0)

        # Enter the main loop
        while True:
            self.print_menu(stdscr, options, current_option)
            key = stdscr.getch()

            if key == curses.KEY_ENTER or key == 10:  # Enter key
                action = options[current_option][1]
                curses.endwin()  # Cleanup curses before calling action
                action(stdscr)
            elif key == curses.KEY_UP:
                current_option = (current_option - 1) % len(options)
            elif key == curses.KEY_DOWN:
                current_option = (current_option + 1) % len(options)
            elif key == 3:  # Ctrl+C (Exit)
                curses.endwin()  # Cleanup curses before exiting
                sys.exit()

    def print_menu(self, stdscr, options, current_option):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for i, option in enumerate(options):
            x = width // 2 - len(option[0]) // 2
            y = height // 2 - len(options) // 2 + i
            if i == current_option:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, option[0])
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option[0])

        stdscr.refresh()

    # Submenu for Setup
    def setup_submenu(self, stdscr):
        current_option = 0
        options = [
            ("Option 1", self.handle_option1),
            ("Option 2", self.handle_option2),
            ("Back", self.handle)
        ]
        self.submenu(stdscr, options, current_option)

    # Submenu for Delete
    def delete_submenu(self, stdscr):
        current_option = 0
        options = [
            ("Option 1", self.handle_option1),
            ("Option 2", self.handle_option2),
            ("Back", self.handle)
        ]
        self.submenu(stdscr, options, current_option)

    # Submenu for Tools
    def tools_submenu(self, stdscr):
        current_option = 0
        options = [
            ("Option 1", self.handle_option1),
            ("Option 2", self.handle_option2),
            ("Back", self.handle)
        ]
        self.submenu(stdscr, options, current_option)

    def submenu(self, stdscr, options, current_option):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        stdscr.clear()

        while True:
            self.print_menu(stdscr, options, current_option)
            key = stdscr.getch()

            if key == curses.KEY_ENTER or key == 10:  # Enter key
                action = options[current_option][1]
                curses.endwin()  # Cleanup curses before calling action
                action(stdscr)
                break
            elif key == curses.KEY_UP:
                current_option = (current_option - 1) % len(options)
            elif key == curses.KEY_DOWN:
                current_option = (current_option + 1) % len(options)
            elif key == 3:  # Ctrl+C (Exit)
                curses.endwin()  # Cleanup curses before exiting
                sys.exit()

    # Sample methods for each menu option
    def handle_option1(self, stdscr):
        self.stdout.write("Option 1 method executed.")
        input("Press any key to continue...")
        
    def handle_option2(self, stdscr):
        self.stdout.write("Option 2 method executed.")
        input("Press any key to continue...")
