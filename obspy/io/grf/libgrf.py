import sys


def is_grf(fp):
    pos = fp.tell()
    header = fp.read(6)
    fp.seek(pos)

    magic = header[0:3]
    version = int.from_bytes(header[3:4], sys.byteorder)
    size = int.from_bytes(header[4:6], sys.byteorder, signed=False)

    if magic != b"GRF":
        raise TypeError("File is not in GRF format.")
    elif version != 1:
        raise TypeError("File version is not supported.")
    elif size < 13:
        raise TypeError("Malformed packet size in header.")


def read_header(fp):
    header = fp.read(13)
    hdict = {
    "magic": header[0:3],
    "version": int.from_bytes(header[3:4], sys.byteorder),
    "size": int.from_bytes(header[4:6], sys.byteorder, signed=False),
    "seq": int.from_bytes(header[6:8], sys.byteorder, signed=False),
    "unit": int.from_bytes(header[8:12], sys.byteorder, signed=False),
    "type": int.from_bytes(header[3:4], sys.byteorder),
    }

    return hdict


def read_packet(fp):
    header = read_header(fp)


def read_grf(fp):
    pass
