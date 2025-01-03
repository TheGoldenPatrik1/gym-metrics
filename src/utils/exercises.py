LOWER = 'Lower'
UPPER = 'Upper'

PUSH = 'Push'
PULL = 'Pull'

QUADS = 'Quadriceps'
HAMSTRINGS = 'Hamstrings'
GLUTES = 'Glutes'
CALVES = 'Calves'
CHEST = 'Chest'
BACK = 'Back'
SHOULDERS = 'Shoulders'
TRICEPS = 'Triceps'
BICEPS = 'Biceps'
FOREARMS = 'Forearms'
ABS = 'Abs'

def get_exercise_classes(exercise):
    exercise = exercise.lower()
    classes = {
        'split': None,
        'group': None,
        'muscles': []
    }

    if 'squat' in exercise or 'leg press' in exercise or 'lunge' in exercise:
        classes['split'] = LOWER
        classes['muscles'] = [QUADS, HAMSTRINGS, GLUTES]
    elif 'nordic' in exercise or 'romanian' in exercise or 'straight leg deadlift' in exercise or 'leg curl' in exercise:
        classes['split'] = LOWER
        classes['muscles'] = [HAMSTRINGS]
    elif 'hammer' in exercise or 'forearm' in exercise:
        classes['split'] = UPPER
        classes['group'] = PULL
        classes['muscles'] = [BICEPS, FOREARMS]
    elif 'deadlift' in exercise:
        classes['split'] = LOWER
        classes['muscles'] = [HAMSTRINGS, GLUTES, BACK]
    elif 'bench' in exercise or 'dips' in exercise:
        classes['split'] = UPPER
        classes['group'] = PUSH
        classes['muscles'] = [CHEST, TRICEPS]
    elif 'overhead' in exercise:
        classes['split'] = UPPER
        classes['group'] = PUSH
        classes['muscles'] = [SHOULDERS, TRICEPS]
    elif 'tricep' in exercise:
        classes['split'] = UPPER
        classes['group'] = PUSH
        classes['muscles'] = [TRICEPS]
    elif 'bicep' in exercise or 'curl' in exercise:
        classes['split'] = UPPER
        classes['group'] = PULL
        classes['muscles'] = [BICEPS]
    elif 'chest' in exercise or 'incline' in exercise or 'decline' in exercise:
        classes['split'] = UPPER
        classes['group'] = PUSH
        classes['muscles'] = [CHEST]
    elif 'row' in exercise or 'lat' in exercise or 'pull' in exercise:
        classes['split'] = UPPER
        classes['group'] = PULL
        classes['muscles'] = [BACK, BICEPS]
    elif 'ab' in exercise or 'crunch' in exercise or 'leg raise' in exercise:
        classes['split'] = UPPER
        classes['muscles'] = [ABS]
    elif 'calf' in exercise:
        classes['split'] = LOWER
        classes['muscles'] = [CALVES]
    elif 'shrug' in exercise or 'lateral' in exercise:
        classes['split'] = UPPER
        classes['group'] = PULL
        classes['muscles'] = [SHOULDERS]
    elif 'sus' in exercise or 'glute' in exercise or 'hip' in exercise or 'ductor' in exercise:
        classes['split'] = LOWER
        classes['muscles'] = [GLUTES]
    elif 'quad' in exercise or 'leg extension' in exercise:
        classes['split'] = LOWER
        classes['muscles'] = [QUADS]

    return classes

def get_class(name):
    splits = [LOWER, UPPER]
    groups = [PUSH, PULL]
    muscles = [QUADS, HAMSTRINGS, GLUTES, CALVES, CHEST, BACK, SHOULDERS, TRICEPS, BICEPS, FOREARMS, ABS]
    
    if name in splits:
        return 'split'
    elif name in groups:
        return 'group'
    elif name in muscles:
        return 'muscles'
    else:
        return 'exercise'