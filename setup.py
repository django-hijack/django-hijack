#!/usr/bin/env python
import distutils
import glob
import os
import subprocess  # nosec
from distutils.cmd import Command
from distutils.command.build import build as _build

from setuptools import setup
from setuptools.command.develop import develop as _develop
from setuptools.command.install_lib import install_lib as _install_lib

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))


class compile_translations(Command):
    description = "Compile i18n translations using gettext."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        pattern = "hijack/locale/*/LC_MESSAGES/django.po"
        for file in glob.glob(pattern):
            name, ext = os.path.splitext(file)
            cmd = ["msgfmt", "-c", "-o", f"{name}.mo", file]
            self.announce(
                "running command: %s" % " ".join(cmd), level=distutils.log.INFO
            )
            subprocess.check_call(cmd, cwd=BASE_DIR)  # nosec


class compile_scss(Command):
    description = "Compile SCSS files using postcss."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cmd = ["npm", "ci"]
        self.announce("running command: %s" % " ".join(cmd), level=distutils.log.INFO)
        subprocess.check_call(cmd, cwd=BASE_DIR)  # nosec

        cmd = ["npm", "run", "build"]
        self.announce("running command: %s" % " ".join(cmd), level=distutils.log.INFO)
        subprocess.check_call(cmd, cwd=BASE_DIR)  # nosec


class build(_build):
    sub_commands = [
        ("compile_translations", None),
        ("compile_scss", None),
    ] + _build.sub_commands


class install_lib(_install_lib):
    def run(self):
        self.run_command("compile_translations")
        self.run_command("compile_scss")
        _install_lib.run(self)


class develop(_develop):
    def run(self):
        self.run_command("compile_translations")
        self.run_command("compile_scss")
        _develop.run(self)


setup(
    name="django-hijack",
    use_scm_version=True,
    cmdclass={
        "build": build,
        "develop": develop,
        "install_lib": install_lib,
        "compile_translations": compile_translations,
        "compile_scss": compile_scss,
    },
)
