import argparse
import json
import random
import os
from datetime import datetime, timedelta

def build_exercises(benchmarks, accessories):
    exercises = {}
    for exercise, benchmark in benchmarks.items():
        if random.random() < 0.4:
            continue
        if random.random() < 0.5:
            weight = benchmark
            reps = random.randint(7, 10)
        else:
            weight = int(benchmark * 1.1)
            reps = random.randint(3, 6)
        if random.random() < 0.2:
            benchmarks[exercise] += int(benchmark * 0.01 + 0.5)
        exercises[exercise] = {
            'weight': weight,
            'reps': reps,
            'sets': random.randint(2, 5)
        }
    for accessory in accessories:
        if random.random() < 0.3:
            exercises[accessory] = True
    return exercises

def generate_example_data(args):
    data = []

    benchmarks = {
        'Bench': random.randint(125, 175),
        'Squat': random.randint(175, 250),
        'Deadlift': random.randint(200, 275),
        'Overhead Press': random.randint(50, 100),
        'Barbell Row': random.randint(100, 150)
    }

    accessories = ['Bicep Curls', 'Tricep Extensions', 'Leg Curls', 'Leg Extensions', 'Calf Raises', 'Pull-ups', 'Dips', 'Incline Machine', 'Row Machine', 'Crunches', 'Lateral Raises']

    start_date = datetime(2022, 1, 1)

    for _ in range(random.randint(200, 400)):
        date = start_date.strftime('%Y-%m-%d')
        start_date += timedelta(days=random.randint(1, 4))
        exercises = build_exercises(benchmarks, accessories)
        data.append({
            'date': date,
            'exercises': exercises
        })

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool to create an example JSON data file.')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to the output JSON file.')
    args = parser.parse_args()

    generate_example_data(args)