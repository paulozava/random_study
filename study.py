from random import choice
from os import stat
from json import load as json_load
from json import dump as json_dump

class Study():
    weighted_dict: dict

    def __init__(self, available_hours=30, daily_hours=6, max_study_stuff_daily=2, max_study_hours_daily=4):
        self.available_hours = available_hours
        self.daily_hours = daily_hours
        self.max_study_stuff_daily = max_study_stuff_daily
        self.max_study_hours_daily = max_study_hours_daily
        self.weighted_dict = self.import_data()

    def import_data(self):
        if stat('stuff_in_use.json').st_size <= 4:
            plan_of_study = open('study_stuff.json')
            plans = json_load(plan_of_study)
            plan_of_study.close()
            total_weight = sum(plans.values())
            hours_weighted = self.available_hours / total_weight
            weighted_dict = {key: (value * hours_weighted) for key, value in plans.items()}
        else:
            plan_of_study = open('stuff_in_use.json')
            weighted_dict = json_load(plan_of_study)
            plan_of_study.close()
        return weighted_dict

    def persist(self):
        persistent = open('stuff_in_use.json', 'w')
        json_dump(self.weighted_dict, persistent)
        persistent.close()

    def pick_one(self):
        picked = choice(list(self.weighted_dict.keys()))
        study_time = self.weighted_dict[picked]

        if study_time > self.max_study_hours_daily:
            study_time = self.max_study_hours_daily

        return picked, study_time
        
    def choose_stuff(self):
        template = 'You have to study {} for {} hours and {} minutes'

        while self.max_study_stuff_daily > 0:
            try:
                picked, study_time = self.pick_one()
                self.weighted_dict[picked] -= study_time
                if self.weighted_dict[picked] <= 0:
                    self.weighted_dict.pop(picked)
                self.daily_hours -= study_time
                self.max_study_stuff_daily -= 1

                hours = int(study_time)
                minutes = int((study_time - hours) * 60)

                print(template.format(picked, hours, minutes))
            except:
                if self.renew_cycle(): break

    def renew_cycle(self):
        response = input('\nThe study stuff has ended, do you want to restart the cycle? [y/n]: ')
        if response in ('y', 'Y'):
            self.reset()
            self.weighted_dict = self.import_data()
            return False
        else:
            return True

    @staticmethod
    def reset():
        persistent = open('stuff_in_use.json', 'w')
        json_dump({}, persistent)
        persistent.close()

