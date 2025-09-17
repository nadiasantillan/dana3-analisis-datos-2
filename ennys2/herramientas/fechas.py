def edad(fecha_nacimiento, fecha):
    res = fecha.year - fecha_nacimiento.year
    if fecha.month < fecha_nacimiento.month:
        res -= 1
    elif fecha.month == fecha_nacimiento.month and fecha.day < fecha_nacimiento.day:
        res -= 1
    return res

def edad_meses(fecha_nacimiento, fecha):
    res = edad(fecha_nacimiento, fecha)*12 + (fecha.month - fecha_nacimiento.month)%12
    if fecha.day < fecha_nacimiento.day:
        res -= 1
    return res