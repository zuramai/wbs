#!C:\Users\ahmad\PycharmProjects\wasap\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'dump==0.0.5','console_scripts','dump'
__requires__ = 'dump==0.0.5'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('dump==0.0.5', 'console_scripts', 'dump')()
    )
