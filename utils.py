import re
import os

def get_period_with_displacement(period):
    displacement = 26
    period_type_part = re.search(r'\D+', period).group()
    period_number_part = int(re.search(r'\d+', period).group())
    if period_type_part == 'mo':
        period_in_days = period_number_part * 31 + displacement
        return str(period_in_days) +'d'
    elif period_type_part == 'd' and period_number_part > 30:
        period_in_days = period_number_part + displacement
        return str(period_in_days) +'d'
    elif period_type_part == 'd' or period_type_part == 'm':
        print ("The Ichimoku Cloud can be plotted for a period >= 1 month")
        return period
    return period

def create_dir_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)