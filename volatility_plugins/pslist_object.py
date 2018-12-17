#List process of Dump RAM WinXP using objects
import volatility.utils as utils
import volatility.commands as commands
import volatility.obj as obj
import struct

class z_kdversionblock_v2(commands.Command):
    """Print _KPCR.KdVersionBlock """

    def render_text(self, outfd, data):
        pass

    def calculate(self):
        addrKPCR = 0xFFDFF000
        addr_space = utils.load_as(self._config)
        data = addr_space.read((addrKPCR+0x34),0x04)
        if not data or len(data) != 0x04:
                debug.error("Failed to read KdVersionBlock")
        (val, ) = struct.unpack("I",data)
        print("struct.unpack() : _KPCR.KdeVersionBlock {0:#8X}".format(val))
        
        KPCR = obj.Object("_KPCR",addrKPCR, addr_space)
        KdVersionBlock = KPCR.KdVersionBlock
        print("obj.Object() : _KPCR.KdeVersionBlock {0:#8X}".format(KdVersionBlock))
        
        # KdVersionBlock + 0x20 
        DBGKD = obj.Object("_DBGKD_GET_VERSION64",KdVersionBlock+0x20, addr_space)
        DebuggerDataList = DBGKD.DebuggerDataList & 0xFFFFFFFF
        print("DebuggerDataList {0:#8X}".format(DebuggerDataList))
        
        # KdVersionBlock+0x20
        LIST_ENTRY = obj.Object("_LIST_ENTRY",KdVersionBlock+0x20, addr_space)
        Flink = LIST_ENTRY.Flink
        print("Flink {0:#8X}".format(Flink))
        
        #flink + 50 = 0x80677ef4+0x50 
        Flink_data = addr_space.read(Flink,0x04)
        (val, ) = struct.unpack("I",Flink_data)
        print("Read value of Flink {0:#8X}".format(val))
        
        
        Flink_data_data = addr_space.read(val+0x50,0x04)
        (val, ) = struct.unpack("I",Flink_data_data)
        print("Read value of Flink data {0:#8X}".format(val))
        
        #EPROCESS
        AddrsPROCESS = val-0x88
        listAddrs = list()
        
        while AddrsPROCESS not in listAddrs:
            listAddrs.append(AddrsPROCESS)
            EPROCESS = obj.Object("_EPROCESS",AddrsPROCESS, addr_space)
            ps = EPROCESS.ImageFileName
            print(ps)
            AddrsPROCESS = EPROCESS.ActiveProcessLinks.Flink-0x88

        
