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

This program makes use of python's ability to open, compile, and execute code found in external files -- at runtime.  This allows external python fragments -- that must, in general, be well-behaved with respect to the menu program itself -- to be added to the host and then automatically incorporated into the menu system -- by the menu-system itself -- to become new menu options.  The only criteria is that the files containing these fragment have executable permission, get located into a pre-defined directory, and have their file names, (and a bit of other metadata), included in a menu options configuration text file  This allows the menu system to be self-updating, incorporating new menu options without the need to modify the menu system code itself.  These options are not separate programs, running in separate processes with their own interpreter, but are incorporated at runtime into the existing execution environment.

The one drawback to this approach is the use of external python libraries; libraries that are required by the external program fragments must be "in" the menu system environment itself, and must, therefore, be "used" in the menu system program.  Hence, many libraries are loaded by the menu-system that it does not appear to need.  As these requirements are not known by python until run-time, debuggers and syntax checkers, (such as pyflakes), will complain bitterly about them.
