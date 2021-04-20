def extract(aircraf):
    x = -1
    raw = []
    for k in aircraf:
        x = x + 1
        raw.append("")
        raw[x] = aircraf[x].split(",")
    return raw

def conco(rada):
    from . import geometry
    coos = []
    x = -1
    for m in range(0,len(rada)):
        x = x + 1
        coos.append("")
        coos[x] = geometry.deg_sysco(rada[x][0], rada[x][1])
    return coos

def plane_type(rada):
    x = -1
    types = []
    numbers = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    clearnames = ["(Moto-) Glider  ","Tow plane       ","Helicopter      ","Parachute       ","Drop plane      ","Hang-glider     ","Para-glider     ","Powered aircraft","Jet aircraft    ","UFO             ","Balloon         ","Airship         ","UAV             ","Ground support  ","Static object   "]

    numbi = [numbers[0]]
    nami = [clearnames[0]]
    for o in range(0,len(rada)):
        x = x + 1
        types.append("")
        types[x] = rada[x][10]
        for p in range(0,15):
            if types[x] == numbi:
                break
            numbi = numbers[p]
            nami = clearnames[p]
        types[x]= nami
    return types

def altitude_info(rada):
    from . import settings
    set_hxml = settings.getvar()
    altinfo = []
    for r in range(0,len(rada)):
        altinfo.append([""]*2)
        altinfo[r][0] = int(rada[r][4]) - int(set_hxml[6])

        altinfo[r][1] = "Fehler     "
        if altinfo[r][0] > 400:
            altinfo[r][1] = "Frei       "
        elif altinfo[r][0] < 401:
            altinfo[r][1] = "Platzrunde "
            if altinfo[r][0] <= 150:
                altinfo[r][1] = "Muss landen"
                if altinfo[r][0] < 11:
                    altinfo[r][1] = "Steht      "
        altinfo[r][0] = str(altinfo[r][0]) + "m"
        while len(altinfo[r][0]) < 7:
            altinfo[r][0] = altinfo[r][0] + " "

    return altinfo

def plane_recognition(rada):
    x = len(rada)
    na = []
    name = []
    ids = []
    ret = []
    for p in range(0,x):
        na.append(rada[p][2])
        ids.append(rada[p][12])
        name.append(rada[p][3])
        #ogn sign / contest sign                    / Short sign
        #Official sign                              / Official sign
        #FLARM device-id                            / Device-ID
        if ids[p] == "0":     #OGN-network was told to not tell identity
            name[p] = "Stealth 1  "
            na[p] = "/   "
        elif ids[p] == "3E6072":
            name[p] = "SF-25      "
            na[p] = "?   "
        elif ids[p] == "DD50F6":
            name[p] = "LS-4       "
            na[p] = "AP  "
        elif ids[p] == "DD9112":
            name[p] = "Jeans Astir"
            na[p] = "OT  "
        elif ids[p] == "DD94A8":
            name[p] = "Jeans Astir"
            na[p] = "Pb  "
        elif ids[p] == "DDA489":
            name[p] = "ASK-21     "
            na[p] = "M1  "
        elif ids[p] == "DDA5DA":
            name[p] = "LS-8       "
            na[p] = "SM  "
        elif ids[p] == "DDA856":
            name[p] = "DG-1000    "
            na[p] = "ICH "
        elif ids[p] == "DDAD1B":
            name[p] = "LS-4       "
            na[p] = "AM  "
        elif ids[p] == "DDDD64":
            name[p] = "D-KICE     "
            na[p] = "CE  "
        else:
            while len(name[p]) < 11:
                name[p] = name[p] + " "
            while len(na[p]) < 4:
                na[p] = na[p] + " "
        ret.append([na[p], name[p],ids[p]])
    return ret
