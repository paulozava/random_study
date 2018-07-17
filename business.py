from study import Study
from os import system
from os import name as system_name
from json import load as json_load
from json import dump as json_dump


class BusinessRules():
    def __init__(self):
        self.configs = self.import_config()
        self.study = Study(*self.configs.values())


    def run(self):
        interact = None
        while interact not in ('e', 'E'):
            self.clear_window()
            self.opening()
            interact = self.options()
            if interact is '1':
                self.refresh_StudyPicker()
                self.study.choose_stuff()
                self.study.persist()
                print('\nPress E to exit or anything else to return the menu?')
                interact = input()
            elif interact is '2':
                sure = input('Are you sure? [y/n]: ')
                if sure is 'y':
                    self.study.reset()
                    print('reseated')
                print('\nPress E to exit or anything else to return the menu?')
                interact = input()
            elif interact in ('c', 'C'):
                self.config()

        print('\n\n')
        print(' ................. Have a good day of study! ................. ')

    def refresh_StudyPicker (self):
        self.study = Study(*self.configs.values())

    def config (self):
        self.clear_window()
        self.opening()
        print('Confuration mode:')
        working = True
        while working:
            print('\nWe have these configs:')
            for key, value in self.configs.items():
                print('The {} [actual: {}]: '.format(key, value), end=' ')
                change = input()
                if change.isdigit():
                    self.configs[key] = float(change)
                print('')
            option = input('Do you want to save(y) or exit(e)?')
            if option in ('y', 'Y'):
                self.config_persist()
                working = False
            elif option in ('e', 'E'):
                working = False

    def config_persist(self):
        configs_json = open('config.json', 'w')
        json_dump(self.configs, configs_json)
        configs_json.close()

    @staticmethod
    def import_config():
        configs_json = open('config.json')
        configs = json_load(configs_json)
        configs_json.close()
        return configs

    @staticmethod
    def opening():
        logo='   _____ _             _         _____ _      _ \n  / ____| |           | |       |  __ (_)    | |            \n | (___ | |_ _   _  __| |_   _  | |__) |  ___| | _____ _ __ \n  \___ \| __| | | |/ _` | | | | |  ___/ |/ __| |/ / _ \ \'__|\n  ____) | |_| |_| | (_| | |_| | | |   | | (__|   <  __/ |   \n |_____/ \__|\__,_|\__,_|\__, | |_|   |_|\___|_|\_\___|_|   \n                          __/ |                             \n                         |___/                              \n'
        print(logo)

    @staticmethod
    def options():
        options = ['1 - Just pick the today\'s study stuff',
                   '2 - Reset the week schedule',
                   'C - Configuration',
                   'E - Exit']
        print('What do you want do do?')
        print(*options, sep='\n')
        interact = input()
        return interact

    @staticmethod
    def clear_window():
        system('cls' if system_name == 'nt' else 'clear')
