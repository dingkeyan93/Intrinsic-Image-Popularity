import os
from dotenv import load_dotenv

for env_file in ['.env']:
    env = os.path.join(os.getcwd(), env_file)
    if os.path.exists(env):
        load_dotenv(env)

capture_output = True