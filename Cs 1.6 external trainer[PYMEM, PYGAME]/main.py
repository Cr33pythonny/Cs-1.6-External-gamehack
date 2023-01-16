from functions import AIMBOT,ESP,ddrun,bhop,updateent
from config_parser import get_value_from_cfg
from multiprocessing import Process





def main():

    
    Process(target=AIMBOT).start()

    Process(target=updateent).start()
    if get_value_from_cfg('ESP','MISC'):
        Process(target=ESP).start()

    if get_value_from_cfg('BHOP','MISC'):
        Process(target=bhop).start()
        
    if get_value_from_cfg('DDRUN','MISC'):
        Process(target=ddrun).start()
    
        

        

        

if __name__ == "__main__":
    main()
