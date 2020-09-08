import numpy as np

from obspy import Stream, Trace
from . import libgrf

def _is_grf(path):
    """
    Tests if the file referred to by path contains a valid GRF packet

    :type path: string
    :param path: A valid filepath to a file to check
    """
    try:
        with open(filename, 'rb') as f:
            libgrf.is_grf(f)
    except Exception:
        return False
    return True

def _read_grf(path):
    """
    Reads a file containing GRF packets

    :type path: string
    :param path: a valid filepath to a file containing GRF packets
    """
    with open(filename, "rb") as fp:
        stream = libgcf.read_grf(fp)
    return stream
