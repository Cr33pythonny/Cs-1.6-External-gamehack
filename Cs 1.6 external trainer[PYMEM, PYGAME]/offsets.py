import pymem
import pymem.process
pm = pymem.Pymem("hl.exe")

hw = pymem.process.module_from_name(pm.process_handle, "hw.dll").lpBaseOfDll
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll


HWview_matrix = (0xEC9780)
HWEntity = (0x120461C)
HWVec3 = (0x658840)
HWResolution = (0xAB779C)
CLMyTeamNumber = (0x100DF4)
hwZOOMING = (0xEC9E20)


