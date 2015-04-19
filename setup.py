from distutils.core import setup
import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    name='JointPurchasesAssistant',
    version='0.0.0.0',
    packages=[''],
    url='',
    license='GPLv3',
    author='PanteR',
    author_email='panter.dsd@gmail.com',
    description='',
    options = {"build_exe": build_exe_options},
    executables = [Executable("__main__.py", base=base, targetName="jointpurchasesassistant.exe")]
)
