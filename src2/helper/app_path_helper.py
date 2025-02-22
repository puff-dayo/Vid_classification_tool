import os
import sys

EXE_PATH = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
EXE_PATH = os.path.normpath(os.path.join(EXE_PATH, "../"))

TEMP_PATH = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.normpath(os.path.join(TEMP_PATH, "../"))

RES_PATH = os.path.join(TEMP_PATH, 'resource')

CONFIG_FILE_NAME = "config.cfg"
CONFIG_FILE = os.path.join(EXE_PATH, CONFIG_FILE_NAME)

if __name__ == '__main__':
    print(EXE_PATH)
    print(TEMP_PATH)