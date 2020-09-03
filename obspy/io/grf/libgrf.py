
def is_grf(fp):
    pos = fp.tell()
    magic = fp.read(3)
    fp.seek(pos)
    if magic != b"GRF":
        raise TypeError("File is not in GRF format.")


def read_grf(fp):
    pass
