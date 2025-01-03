from .exercises import get_exercise_classes

def parse_classes(classes, exercise_classes, cls):
    if cls not in exercise_classes or exercise_classes[cls] == None:
        return
    arr = exercise_classes[cls] if cls == 'muscles' else [exercise_classes[cls]]
    for item in arr:
        if item not in classes[cls]:
            classes[cls][item] = 0
        classes[cls][item] += 1

def load_classes(data):
    classes = {
        'split': {},
        'group': {},
        'muscles': {}
    }

    for item in data:
        for exercise in item['exercises'].keys():
            exercise_classes = get_exercise_classes(exercise)
            for cls in classes.keys():
                parse_classes(classes, exercise_classes, cls)
                    
    return classes['split'], classes['group'], classes['muscles']

def load_exercises(data):
    exercises = {}
    for item in data:
        for key in item['exercises'].keys():
            if key in exercises:
                exercises[key] += 1
            else:
                exercises[key] = 1
    return exercises