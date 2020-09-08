import sys
import numpy as np


def is_grf(fp):
    """
    Checks if a GRF packet is valid

    :type fp: file
    :param fp: A file object pointing to the common header of a GRF packet
    """
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
        raise TypeError("Malformed packet size in GRF header.")


def read_header(fp):
    """
    Read the 13 byte header that wraps all GRF packets

    :type fp: file
    :param fp: File object containing GRF data
    """
    header = fp.read(13)
    hdict = {
        "magic": header[1:3],
        "version": header[3:4], # 1 byte
        "size": header[4:6],    # 2 bytes
        "seq": header[6:8],     # 2 bytes
        "unit": header[8:12],   # 4 bytes
        "type": header[12:14],  # 1 byte
    }

    return hdict


def decode_waveform_int32(waveform):
    """
    Decodes a waveform stored as a signed 32-bit integer

    :type waveform: bytes
    :param waveform: A bytes object with len % 4 == 0
    """
    try:
        with memoryview(waveform) as m:
            return np.array(m.cast("i"), dtype=np.int32)
    except Exception:
        return np.empty(0, dtype=np.int32)


def decode_waveform_int24(waveform):
    """
    Decodes a waveform stored as a signed 24-bit integer

    :type waveform: bytes
    :param waveform: A bytes object with len % 3 == 0
    """
    data = []
    for i in range(0, len(waveform), 3):
        x = int.from_bytes(waveform[i:i + 3], sys.byteorder)
        data.append(x)
    return np.array(data, dtype=np.int32)


def decode_waveform_cm8(waveform):
    """
    Decodes a waveform compressed using the CM8 algorithm.

    :type waveform: bytes
    :param waveform: A bytes object containing the compressed data
    """
    pass


def parse_data_packet(packet):
    """
    Parses a GRF data packet and returns the header and decoded data

    :type packet: bytes
    :param packet: A bytes object containing the GRF packet and header
    """
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
        "num_samples": header[73:75],
    }

    decoders = {
        0: decode_waveform_int32,
        1: decode_waveform_int24,
        2: decode_waveform_cm8,
    }

    try:
        datatype = int.from_bytes(hd["datatype"], sys.byteorder)
        data = decoders[datatype](packet[75:])
        return hd, data
    except KeyError as e:
        pass

    return hd, None


def read_packet(fp):
    """
    Reads a packet and decodes it using the appropriate handler

    :type fp: file
    :param fp: A file object pointing to the GRF packet to be read
    """
    handlers = {
        0: lambda _: [],
        1: parse_data_packet,
    }

    header = read_header(fp)
    packet_data = fp.read(header["size"] - 13)

    packet_type = int.from_bytes(header["type"], sys.byteorder)
    if packet_type in handlers:
        packet_header, data = handlers[packet_type](packet_data)

    return (header, packet_header, data)


def read_grf(fp):
    """
    Reads a GRF file containing one or more GRF packets

    Currently only supports two packet types: empty, and data.
    Connection packets are not supported.

    :type fp: file
    :param fp: A file object pointing to the first packet in the file
    """
    packets = []
    while True:
        try:
            packets.append(read_packet(fp))
        except EOFError:
            break;
