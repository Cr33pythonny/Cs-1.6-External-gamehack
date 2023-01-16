import os
def find_weapon_settings(weapon_name:str,m:list):
    parse_data = []
    val = 0
    for i in range(len(m)):
        try:
            if weapon_name in m[i][0]:
                parse_data.clear()
                val = 0
                continue
            
            if val !=3:
                parse_data.append(m[i][0])
                val +=1
        except(TypeError):
            continue

    return parse_data

def get_value_from_cfg(search:str,weapon_name:str):
    mass = get_split_strings()
    new_list = find_weapon_settings(weapon_name,mass)
    for i in new_list:
        if search in i:
            if '=' in i:
                return int(i.split('=')[1])



def get_split_strings():
    m = []
    dir = os.path.abspath(__file__).replace('config_parser.py', 'settings.ini')
    with open(dir,'r',encoding='utf-8')as r:
        for i in r:

            m.append(i.split('\n'))
    return m


def get_current_weapon(id:int):
    if id == 29:
        return 'KNIFE'
    elif id == 26:
        return 'DEAGLE'
    elif id == 16:
        return 'USP'
    elif id == 17:
        return 'GLOCK'
    elif id == 22:
        return 'M4A1'
    elif id == 28:
        return 'AK-47'
    elif id == 14:
        return 'GALIL'
    elif id == 15:
        return 'FAMAS'
    elif id == 3:
        return 'SCOUT'
    elif id == 18:
        return 'AWP'
    elif id == 27:
        return 'SG-552'
    elif id == 8:
        return 'AUG'
    elif id == 24:
        return 'G3-SG-SNIPER'
    elif id == 13:
        return 'SG-SNIPER'
    elif id == 19:
        return 'MP5'



def main():
    rcs = get_value_from_cfg('RCS','AWP')
    fov = get_value_from_cfg('FOV','AWP')
    smooth = get_value_from_cfg('SMOOTH','AWP')
            
            

    print(f'WEAPON SETTINGS: \n RCS : {rcs} \n FOV: {fov} \n SMOOTH {smooth} \n')

if __name__ == "__main__":
    main()
