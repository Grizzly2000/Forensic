import sys
import struct


class MBR():
    def __init__(self,path):
        self.path=path
        self.parse()

    def parse(self):
        with open(self.path,"rb") as f:
            f.seek(446)
            self.p1 = PartEntry(f.read(16))
            self.p2 = PartEntry(f.read(16))
            self.p3 = PartEntry(f.read(16))
            self.p4 = PartEntry(f.read(16))
            self.boot_sign = f.read(2)

    def print_data(self):
            self.p1.print_data()
            self.p2.print_data()
            self.p3.print_data()
            self.p4.print_data()


class PartEntry():
    def __init__(self, content):
        self.content = content
        self.parse_part()

    def parse_part(self):
        self.bootable = bool(self.content[0] & 0b1000000)
        self.CHS_start = tuple(self.content[1:4])
        self.part_type = self.content[4]
        self.CHS_end = tuple(self.content[5:8])
        (self.part_start, ) = struct.unpack("I", self.content[8:12])
        (self.nb_sectors, ) = struct.unpack("I", self.content[12:16])
        self.part_size = (self.nb_sectors*512)/(1024*1024)

    def print_data(self):
        print("bootable: {}".format(self.bootable))
        print("CHS_start: {}".format(self.CHS_start))
        print("part_type: {}".format(self.part_type))
        print("CHS_end: {}".format(self.CHS_end))
        print("part_start: {}".format(self.part_start))
        print("nb_sectors: {}".format(self.nb_sectors))
        print("part_size: {} Mo".format(self.part_size))
        print()


MBR(sys.argv[1]).print_data()
