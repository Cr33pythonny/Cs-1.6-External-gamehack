from functions import AIMBOT,ESP,ddrun,bhop,updateent
from config_parser import get_value_from_cfg
import multiprocessing 





def main():

    

        multiprocessing.Process(target=AIMBOT).start()

        multiprocessing.Process(target=updateent).start()
        if get_value_from_cfg('ESP','MISC'):
            multiprocessing.Process(target=ESP).start()

        if get_value_from_cfg('BHOP','MISC'):
            multiprocessing.Process(target=bhop).start()
            
        if get_value_from_cfg('DDRUN','MISC'):
            multiprocessing.Process(target=ddrun).start()

    
        

        

        

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
