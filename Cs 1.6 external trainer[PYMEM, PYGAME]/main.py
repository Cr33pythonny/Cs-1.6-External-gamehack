from functions import AIMBOT,ESP,ddrun,bhop,updateent
from config_parser import get_value_from_cfg
import multiprocessing 





def main():

        multiprocessing.Process(target=updateent).start()


        multiprocessing.Process(target=AIMBOT).start()

        if get_value_from_cfg('ESP','MISC',3):
            multiprocessing.Process(target=ESP).start()

        if get_value_from_cfg('BHOP','MISC',3):
            multiprocessing.Process(target=bhop).start()
            
        if get_value_from_cfg('DDRUN','MISC',3):
            multiprocessing.Process(target=ddrun).start()

    
        

        

        

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
