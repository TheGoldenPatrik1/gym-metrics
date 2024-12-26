import json
import argparse
import os
from datetime import datetime
import re

def month_abbrevation_to_full(month):
    _month = month.lower()
    month_map = {
        'jan': 'January',
        'feb': 'February',
        'mar': 'March',
        'apr': 'April',
        'may': 'May',
        'jun': 'June',
        'jul': 'July',
        'aug': 'August',
        'sep': 'September',
        'oct': 'October',
        'nov': 'November',
        'dec': 'December'
    }
    if _month in month_map:
        return month_map[_month]
    else:
        return month

def process_exercise_name(name, exercises, parent=None):
    name_map = {
        "Extension": "Tricep Extensions",
        "Extensions": "Tricep Extensions",
        "Tricep Extension": "Tricep Extensions",
        "Pushdown": "Tricep Pushdowns",
        "Pushdowns": "Tricep Pushdowns",
        "Tricep Pushdown": "Tricep Pushdowns",
        "Overhead": "Overhead Press",
        "Cable Biceps": "Cable Bicep Curls",
        "Trap DL": "Trap Bar Deadlift",
        "Trap Bar DL": "Trap Bar Deadlift",
        "Dip": "Dips",
        "Leg Ext": "Leg Extensions",
        "Pull-up": "Pull-ups",
        "Cable Row": "Cable Rows",
        "Wide Cable Row": "Wide Cable Rows",
        "High Row": "Row Machine",
        "High Row Machine": "Row Machine",
        "Leg Extension": "Leg Extensions",
        "Leg Curl": "Leg Curls",
        "Iso Lateral Row": "Row Machine",
        "Pec Machine": "Bench Machine",
        "Press Machine": "Bench Machine",
        "Chest": f"Chest {parent}",
        "Hi": f"High {parent}",
        "High": f"High {parent}",
        "Lo": f"Low {parent}",
        "Low": f"Low {parent}", 
        "Seated Calf": "Seated Calf Machine",
        "Standing Calf": "Standing Calf Machine",
        "Straight Leg RDL": "Straight Leg Deadlift",
        "Row Cable": "Cable Rows",
        "Row": "Rows",
        "Barbell Calf": "Barbell Calf Raises",
        "Barbell Calf Raise": "Barbell Calf Raises",
        "Incline Smith": "Incline Smith Machine",
        "Lat Pulldown": "Lat Pulldowns",
        "Incline": "Incline Bench",
        "Flies Machine": "Chest Flies",
        "Calf Raise": "Barbell Calf Raises",
        "Rows": "Barbell Rows",
        "Barbell Bicep Curls": "Bicep Curls",
        "Dumbbell Row": "Dumbbell Rows"
    }
    if name in name_map:
        name = name_map[name]
    name = name.replace("Flys", "Flies").replace("Fly", "Flies").replace("Machines", "Machine")
    name = name.replace("DL", "Deadlift").replace("Cable Flies", "Chest Flies")
    if name in name_map:
        name = name_map[name]
    if name not in exercises:
        exercises[name] = 1
    else:
        exercises[name] += 1
    return name

def zip_data(arr):
    if len(arr) == 3:
        middle_split = arr[1].split(', ')
        first_item = [arr[0], middle_split[1]]
        last_item = [middle_split[0], arr[2]]
        zipped_items = zip(first_item, last_item)
        return zipped_items
    else:
        zipped_items = zip([arr[0]], [arr[1]])
        return zipped_items

def parse_exercise_with_data(line, item, exercises):
    name = process_exercise_name(line[0], exercises)
    line = line[1].split(' @ ')
    if line[0] == "Recovery":
        item['exercises'][name] = True
    elif "1RM" in line[0]:
        item['exercises'][name] = {
            '1RM': float(line[1].split(" ")[0])
        }
    else:
        zipped_items = zip_data(line)
        for zip_index, zip_line in enumerate(zipped_items):
            for line_index, line_val in enumerate(zip_line[0].split(', ')):
                sets_and_reps = line_val.split('x')
                sets = sets_and_reps[0]
                for rep_index, rep_value in enumerate(sets_and_reps[1].split(',')):
                    for weight_index, weight_value in enumerate(zip_line[1].split(',')):
                        weight_value = weight_value.strip().split(' ')[0].replace("s", "")
                        obj = {
                            'sets': int(sets),
                            'reps': int(rep_value),
                            'weight': float(weight_value)
                        }
                        if zip_index == 0 and line_index == 0 and weight_index == 0 and rep_index == 0:
                            item['exercises'][name] = obj
                        elif isinstance(item['exercises'][name], list):
                            item['exercises'][name].append(obj)
                        else:
                            item['exercises'][name] = [item['exercises'][name], obj]

def parse_exercise(line, item, exercises):
    line = line.strip()[2:]
    line = line.split(' - ')
    if len(line) == 2:
        # The exercise has set, rep, & weight data
        parse_exercise_with_data(line, item, exercises)
    else:
        # The exercise or exercises do not contain significant additional data
        line = re.split(r' (?:and|&) ', line[0])
        parent = None
        for exercise in list(reversed(line)):
            exercise = exercise.split(' @ ')
            name = process_exercise_name(exercise[0], exercises, parent)
            parent = " ".join(name.split(' ')[1:])
            item['exercises'][name] = { 'weight': float(exercise[1].replace('s', '').replace('+', '')) } if len(exercise) == 2 else True

def parse_date(line):
    # Build the item
    item = {
        'exercises': {}
    }
    if '(High)' in line:
        item['high'] = True
    elif '(Low)' in line:
        item['low'] = True
    if 'Upper' in line:
        item['type'] = 'upper'
    elif 'Lower' in line:
        item['type'] = 'lower'

    # Parse date information from the line
    line = line.split('-')
    date = line[1].strip().split(' ')
    day_of_week = date[0]
    month = month_abbrevation_to_full(date[1])
    day_of_month = date[2]

    return item, day_of_week, month, day_of_month

def process_data(lines):
    data = []
    item = {}
    year = datetime.now().year
    current_month = None
    exercises = {}

    for line in lines:
        if line.startswith('    '):
            # The line contains exercise data
            parse_exercise(line, item, exercises)
        else:
            # The line contains a date
            if item:
                data.append(item)
            item, day_of_week, month, day_of_month = parse_date(line)
            if month != current_month:
                if month == 'December' and current_month == 'January':
                    year -= 1
                current_month = month
            item['date'] = f'{day_of_week} {month} {day_of_month}, {str(year)}'

    # Sort and print the exercises
    sorted_exercises = sorted(exercises.keys())
    for key in sorted_exercises:
        print(f'{key}: {exercises[key]}')
    print(f'Total: {len(exercises)}')

    return data

def data_to_json(args):
    if not os.path.exists(args.input):
        print('File does not exist.')
        return

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    with open(args.input, 'r') as f:
        lines = f.readlines()
        data = process_data(lines)

    with open(args.output, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool to convert textual workout data to JSON.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Path to the input data file.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to the output JSON file.')
    args = parser.parse_args()

    data_to_json(args)