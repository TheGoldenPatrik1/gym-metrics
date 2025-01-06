import os
from dotenv import load_dotenv

load_dotenv()

PULLUPS = os.environ.get('PULLUPS', 'Pull-ups')
OVERHEAD_PRESS = os.environ.get('OVERHEAD_PRESS', 'Overhead Press')
BENCH = os.environ.get('BENCH', 'Bench')
SQUAT = os.environ.get('SQUAT', 'Squat')
DEADLIFT = os.environ.get('DEADLIFT', 'Deadlift')