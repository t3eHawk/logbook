import os
import pip
import sys
import socket
import argparse
import platform

from datetime import datetime

class Data(dict):
    def __getattr__(self, name):
        return self.get(name)

class Sysinfo():
    def __init__(self, logger):
        self.logger = logger
        self.parser = argparse.ArgumentParser()
        self.process(env=True, exe=True)
        pass

    def __str__(self):
        all = [
            f'[Environment variables: {self.env}]',
            f'[Execution variables: {self.exe}]',
            f'[Execution arguments: {self.args.__dict__}]',
            f'[Statistic variables: {self.stat}]']
        return ', '.join(all)

    __repr__ = __str__

    def process(self, env=False, exe=False, args=True, anons=True, stat=True):
        if env is True:
            self.env = Data()
            for key, value in os.environ.items():
                self.env[key.lower()] = value


        if exe is True or args is True or anons is True:
            knowns, unknowns = self.parser.parse_known_args()
            if args is True: self.args = knowns
            if exe is True: self.exe = Data()
            if anons is True: self.anons = []
            for item in unknowns:
                try:
                    key, value = item.split('=')
                except ValueError:
                    if anons is True: self.anons.append(item)
                else:
                    if exe is True: self.exe[key.lower()] = value

        if stat is True:
            self.stat = Data()
            stat = {
                'app':
                    self.logger.app,
                'desc':
                    self.logger.desc,
                'version':
                    self.logger.version,
                'hostname':
                    platform.node(),
                'ip':
                    socket.gethostbyname(socket.gethostname()),
                'user':
                    os.getlogin(),
                'pid':
                    os.getpid(),
                'system':
                    platform.platform(),
                'python':
                    f'{platform.python_version()}-{platform.architecture()[0]}',
                'exec':
                    sys.executable,
                'compiler':
                    platform.python_compiler(),
                'pip':
                    pip.__version__,
                'loctime':
                    datetime.now().isoformat(sep=' ', timespec='seconds')}
            self.stat.update(stat)
        pass

    def configure(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)
        self.process(args=True, stat=False)
        pass
