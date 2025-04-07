# cxfreeze version, but that leaves too many files

from cx_Freeze import setup, Executable
import sys


base = None
if sys.platform == "win32":
    base = "Win32GUI"

executable = [Executable("main.py", base=base, icon="img/goonapplogo", target_name="goonsrb2launcher")]

exe_options = {
    "include_files": ["img"],
}

setup(name = "goonsrb2launcher",
      version = "0.1.1",
      description = "Simple SRB2 launcher, nothing more, nothing less.",
      executables = executable,
      options = {"build_exe": exe_options})

