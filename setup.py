#!/usr/bin/env python
import distutils
import glob
import os
import subprocess  # nosec
from distutils.cmd import Command
from distutils.command.build import build as _build
from distutils.command.install import install as _install

from setuptools import setup

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))


class compile_translations(Command):
    description = "Compile i18n translations using gettext."
    user_options = []

    def initialize_options(self):
        self.build_lib = None

    def finalize_options(self):
        self.set_undefined_options("build", ("build_lib", "build_lib"))

    def run(self):
        pattern = "hijack/locale/*/LC_MESSAGES/django.po"
        for file in glob.glob(pattern):
            name, ext = os.path.splitext(file)
            cmd = ["msgfmt", "-c", "-o", f"{self.build_lib}/{name}.mo", file]
            self.announce(
                "running command: %s" % " ".join(cmd), level=distutils.log.INFO
            )
            subprocess.check_call(cmd, cwd=BASE_DIR)  # nosec


class compile_scss(Command):
    description = "Compile SCSS files using postcss."
    user_options = []

    def initialize_options(self):
        self.build_lib = None

    def finalize_options(self):
        self.set_undefined_options("build", ("build_lib", "build_lib"))

    def run(self):
        cmd = ["npm", "ci"]
        self.announce("running command: %s" % " ".join(cmd), level=distutils.log.INFO)
        subprocess.check_call(cmd, cwd=BASE_DIR)  # nosec

        cmd = ["npm", "run", "build"]
        self.announce("running command: %s" % " ".join(cmd), level=distutils.log.INFO)
        subprocess.check_call(
            cmd, cwd=BASE_DIR, env={**os.environ, "BUILD_LIB": self.build_lib}
        )  # nosec


class build(_build):
    sub_commands = [
        *_build.sub_commands,
        ("compile_translations", None),
        ("compile_scss", None),
    ]


class install(_install):
    sub_commands = [
        *_install.sub_commands,
        ("compile_translations", None),
        ("compile_scss", None),
    ]


setup(
    name="django-hijack",
    use_scm_version=True,
    cmdclass={
        "build": build,
        "install": install,
        "compile_translations": compile_translations,
        "compile_scss": compile_scss,
    },
)
