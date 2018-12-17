#List process of Dump RAM WinXP
import volatility.utils as utils
import volatility.commands as commands
import volatility.obj as obj
import struct

class z_pslist(commands.Command):
    """Print _KPCR.KdVersionBlock"""

    def render_text(self, outfd, data):
        # outfd.write("_KPCR.KdVersionBlock 0x{0:8X}\n".format(data.KdVersionBlock))
        pass

    def calculate(self):
        # KPCR address on WinXP
        addrKPCR = 0xFFDFF000
        # Load a new address space
        addr_space = utils.load_as(self._config)

        KdVersionBlock = addr_space.read((addrKPCR+0x34), 0x04)
        (addrDBGKD, ) = struct.unpack("I", KdVersionBlock)
        print("addrDBGKD: 0x{0:8X}".format(addrDBGKD))
        
        DebuggerDataList = addr_space.read((addrDBGKD+0x20), 0x04)
        (addrListEntry, ) = struct.unpack("I", DebuggerDataList)
        print("addrListEntry: 0x{0:8X}".format(addrListEntry))

        Flink = addr_space.read((addrListEntry), 0x04)
        (addrKDBGDATA, ) = struct.unpack("I", Flink)
        print("addrKDBGDATA: 0x{0:8X}".format(addrKDBGDATA))
        
        PsActiveProcessHead = addr_space.read((addrKDBGDATA+0x50), 0x04)
        (addrEPROCESSoffset, ) = struct.unpack("I", PsActiveProcessHead)
        print("addrEPROCESSoffset: 0x{0:8X}".format(addrEPROCESSoffset))

        addrEPROCESS = addrEPROCESSoffset-0x88
        listAddrs = list()
        
        while addrEPROCESS not in listAddrs:
            listAddrs.append(addrEPROCESS)
            PsName = addr_space.read((addrEPROCESS+0x174), 16)
            print("PsName: {}".format(PsName))
            temp = addr_space.read((addrEPROCESS+0x88), 0x04)
            (addrEPROCESSoffset, ) = struct.unpack("I", temp) 
            addrEPROCESS = addrEPROCESSoffset - 0x88
