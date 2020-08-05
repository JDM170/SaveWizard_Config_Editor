#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import platform
from cx_Freeze import setup, Executable

base = None
if platform == 'win32':
    base = 'Win32GUI'

executables = [Executable('__init__.py', targetName='config_editor.exe', base=base)]

excludes = ['html', 'pydoc_data', 'unittest', 'xml', 'pwd', 'shlex', 'platform', 'webbrowser', 'pydoc', 'tty',
            'inspect', 'doctest', 'plistlib', 'subprocess', 'bz2', '_strptime', 'dummy_threading', 'selectors',
            'select', 'http', 'email', 'datetime', 'calendar', 'urllib', 'posixpath', 'tempfile', 'shutil', 'copy',
            'stringprep', 'socket']

includes = ['pkgutil', 'PyQt5.sip']

zip_include_packages = ['collections', 'encodings', 'importlib', 'json', 'hashlib', 'ast', 'PyQt5', 'main']

include_files = ['dlls/imageformats', 'dlls/platforms', 'dlls/styles']

options = {
    'build_exe': {
        'excludes': excludes,
        'includes': includes,
        'include_msvcr': True,
        'build_exe': 'prog_build',
        'include_files': include_files,
        'zip_include_packages': zip_include_packages,
    }
}

setup(
    name='SaveWizard Config Editor',
    version='1.0',
    description='For editing configs from SaveWizard',
    executables=executables,
    options=options,
    requires=['PyQt5'],
)
