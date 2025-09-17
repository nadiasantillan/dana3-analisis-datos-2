import pandas as pd
from os.path import expanduser
from io import StringIO
import csv
from datetime import date
import logging

class Lector:
    def __init__(self, archivo_datos_nombre):
        self.archivo_datos_nombre = archivo_datos_nombre

    def extracto_variables(self, variables, variables_fecha=None):
        variables_fecha = variables_fecha or []
        temp = StringIO()
        with open(expanduser(self.archivo_datos_nombre), "rt", encoding="utf-8") as f:
            lector = csv.reader(f, skipinitialspace=True)   
            i = 0         
            for registro in lector:
                if i == 0:
                    inexistentes = [variable for variable in variables if variable not in registro]
                    if inexistentes:
                        logging.warning("[%s] Variables inexistentes en %s: %s",
                                        self.__class__.__name__,
                                        self.archivo_datos_nombre,
                                        inexistentes)
                    indices = [registro.index(variable) for variable in variables if variable in registro]
                    i += 1
                valores = [valor for i, valor in enumerate(registro) if i in indices]
                temp.write(f"{','.join(valores)}\n")
        temp.seek(0)

        df = pd.read_csv(temp)
        self._conversion_fechas(variables_fecha, df)
        return df
  
    def _conversion_fechas(self, variables, df):
        for variable in variables:
            df[variable] = df[variable].apply(self._conversion_fecha) 
    
    @staticmethod
    def _conversion_fecha(fecha_cadena):
        res = fecha_cadena
        if isinstance(fecha_cadena, str):
            c = fecha_cadena.split("/")
            if len(c) == 3:
                res = date(int(c[2]), int(c[0]), int(c[1]))

        return res
