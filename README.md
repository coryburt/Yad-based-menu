# Yad-based-menu
A YAD-based menu system for Linux desktops
This is a simple GUI menu system based on the YAD (Yet Another Dialog) utility and the python3 library that exposes its functionality in a "pythonic way."

In addition the afforementioned "yad" library, it imports the following:

  * re, sh, csv, os, notify2, threading, shutil, stat, pwd, tarfile, sys
  * from yad import YAD
  * from collections import namedtuple, OrderedDict
  * from subprocess import check_output, Popen, CalledProcessError
  * from time import sleep
  * from io import StringIO
  * from psutil import disk_partitions
  * from shutil import which
  * from glob import glob

  * from helios_common import GetPasswd, SendNotice, UpdateMounted
  
The "helios_common" module is included in this repository.
Note that several of the libraries loaded are not used in the menu system code itself.  However, the program makes use of python's ability open, compile, and execute code found in external files.  This allows external programs -- written in python and generally well-behaved with respect to the menu program itself -- to be added to the host and then incorporated into the menu system to become new menu options.  The only criteria is that they have executable permission, get located into a pre-defined directory, and have their file names, (and a bit of other metadata), included in the menu options text file  This allows the menu system to be updated with new menu options without needed to modify the menu system itself.

The one drawback to this approach is the use of external python libraries; the libraries that the external programs use must be "used" in the menu system program itself.  Hence, the many libraries that are loaded by the menu-system that it does not appear to need or use.  As these requirements are not known by python until run-time, debuggers and syntax checkers, (such as pyflakes), will issue warnings about loading libraries that are not used.
