import os

from environs import Env


def load_env():
    env = Env()
    env.read_env()

    return env.str("API_KEY"), env.bool("DEBUG", False)


def change_api_key(value):
    # Read the .env file into a dictionary
    env_vars = {}
    with open('.env', 'r') as f:
        for line in f:
            if line:
                key, value = line.split('=')
                env_vars[key] = value
k
    env_vars['API_KEY'] = value

    # Write the updated dictionary back to the .env file
    with open('.env', 'w') as f:
        for key, value in env_vars.items():
            f.write(f'{key}={value}\n')

    return env_vars['API_KEY']


if __name__ == '__main__':
    print(load_env())
    a = change_api_key('test')
    print(a)
    print(load_env())
