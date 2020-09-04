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
    "version": header[3:4], # 1 byte
    "size": header[4:6],    # 2 bytes
    "seq": header[6:8],     # 2 bytes
    "unit": header[8:12],   # 4 bytes
    "type": header[12:14],  # 1 byte
    }

    return hdict


def read_data_packet_header(fp):
    header = fp.read(76)
    # Double check these offsets against the spec
    hd = {
    "channel_number": header[0:2],
    "network": header[2:10],
    "station": header[10:26],
    "component": header[26:34],
    "time_quality": header[34:35],
    "rate_quality": header[35:36],
    "start_time": header[36:44],
    "time_correction": header[44:52],
    "sample_rate": header[52:60],
    "sample_correction"]: header[60:68],
    "cpv": header[68:72],
    "datatype": header[72:73],
    "num_samples": header[73:77],
    }


def read_packet(fp):
    header = read_header(fp)
    packet_data = fp.read(header["size"] - 13)

    return (header, packet_data)


def read_grf(fp):
    while True:
        try:
            packet = read_packet(fp)
        except EOFError:
            break;
