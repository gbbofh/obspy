import numpy as np

from obspy import Stream, Trace
from . import libgrf

def _is_grf(path):
    try:
        with open(filename, 'rb') as f:
            libgrf.is_grf(f)
    except Exception:
        return False
    return True

def _read_grf(path):
    pass

