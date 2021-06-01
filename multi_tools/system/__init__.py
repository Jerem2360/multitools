from multi_tools.system import env
from time import sleep


thread = env.thread

import_module = env.import_module


def wait(time_secs: int or float):
    return sleep(time_secs)


class Module(env.Module):
    @staticmethod
    def is_installed(name: str):
        return env.module_installed(name)

