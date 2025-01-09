# Gym Metrics

This is a powerful self-hosted web dashboard for visualizing your workout data, built with [python](https://www.python.org/) and [panel](https://github.com/holoviz/panel).

<img width="1422" alt="Screenshot 2025-01-09 at 1 47 38 PM" src="https://github.com/user-attachments/assets/5d464de6-f5e1-41cd-8967-b42674ff31bc" />

## Features

- Ability to sort data based on weeks, months, or years
- Multiple inputs for selecting and comparing workouts, splits, body groups, and exercises
- Frequency graph:
<img width="1422" alt="Screenshot 2025-01-09 at 1 48 24 PM" src="https://github.com/user-attachments/assets/86a436ca-823b-492f-9cc5-dee1799f6d71" />

- Weight lifted graph:
<img width="1423" alt="Screenshot 2025-01-09 at 1 48 52 PM" src="https://github.com/user-attachments/assets/ec822e80-757f-4ae4-a787-ae4dec4db8c4" />

- Progress chart, split as necessary between "high" and "low" workouts:
<img width="1422" alt="Screenshot 2025-01-09 at 1 49 32 PM" src="https://github.com/user-attachments/assets/cecbede9-8387-486f-b93f-c44cae1e4c50" />

- Exercise frequency graph:
<img width="1423" alt="Screenshot 2025-01-09 at 1 50 27 PM" src="https://github.com/user-attachments/assets/78712fae-7bce-45d0-aef1-fec886ce4db8" />

- Exercise breakdown for splits and body groups:
<img width="1332" alt="Screenshot 2025-01-09 at 1 51 07 PM" src="https://github.com/user-attachments/assets/66a0b3d4-bd19-46b7-9d8e-a0abb7ac91e6" />


## Getting Started

1. Create a [conda](https://www.anaconda.com/) environment with the dependencies:

```shell
conda env create -f environment.yml
```

2. Activate the new environment:

```shell
conda activate gym-metrics
```

3. Create a randomized example JSON file of workout data:

```shell
python scripts/generate_example_data.py -o data/example.json
```

4. Run the program:

```shell
make
```

## Using Your Own Data

The program accepts a [JSON](https://www.json.org/json-en.html) file containing an array of workouts. Each workout must have two fields:

- `date`: the date on which the workout occured, as a string, in some sort of format that the [python datetime module](https://docs.python.org/3/library/datetime.html) can recognize.
- `exercises`: a dictionary of the exercises in the workout, with the key being the name of the exercise and the value being either `true` or a dictionary with either a `1RM` value or the `sets`, `reps`, and `weight`.

Here is a simple example:

```json
[
    {
        "date": "2022-01-01",
        "exercises": {
            "Bench": {
                "weight": 150,
                "reps": 8,
                "sets": 3
            },
            "Squat": {
                "1RM": 275
            },
            "Pull-ups": true
        }
    }
]
```

Given that your workout data probably isn't in this format and given that this format is not the most convenient for recording your workouts, it may be necessary to create a custom pipeline script for converting your data from its current format to the JSON format that gym-metrics accepts. [This](/scripts/text_to_json.py) is an example pipeline for converting textual data to JSON.

Gym-metrics is largely un-opinionated when it comes to naming conventions, but there are a few features that rely on certain exercise names. You may override [those defaults](/src/constants/exercises.py) using a `.env` file. Here is an example configuration:

```
BENCH="Bench Press"
PULLUPS="Chin Ups"
```
