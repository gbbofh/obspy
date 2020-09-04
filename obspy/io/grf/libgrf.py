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
    """
    Read the 13 byte common header for all GRF packets
    """
    header = fp.read(13)
    hdict = {
    "magic": header[0:3],
    "version": header[3:4], sys.byteorder,              # 1 byte
    "size": header[4:6], sys.byteorder, signed=False,   # 2 bytes
    "seq": header[6:8], sys.byteorder, signed=False,    # 2 bytes
    "unit": header[8:12], sys.byteorder, signed=False,  # 4 bytes
    "type": header[3:4], sys.byteorder,                 # 1 byte
    }

    return hdict


def read_packet(fp):
    header = read_header(fp)
    packet_data = fp.read(header["size")


def read_grf(fp):
    pass
