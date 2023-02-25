from .config import *
try:
    from .mainconfig import *
except Exception as e:
    from .testconfig import *