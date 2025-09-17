import pandas as pd
from os.path import expanduser
from io import StringIO
import csv
from datetime import date
from math import isnan

# from ennys2.lector import Lector
# l = Lector("~/unsl/anadatosii/ennys/ENNyS2_encuesta.csv", "~/unsl/anadatosii/ennys/ennys2_variables.csv")
# df = l.extracto_variables(("E_CUEST","C1_FECHA", "C1_SEXO", "C2_FECHA", "C2_SEXO", "fecha_entr"))
# babies = df[df["E_CUEST"]=="0 a 23 meses"]
# babies[babies["fecha_entr"]-babies["C1_FECHA"]>timedelta(days=180)]


class Lector:
    def __init__(self, archivo_datos_nombre, archivos_variables_nombre):
        self.archivo_datos_nombre = archivo_datos_nombre
        self.archivo_variables_nombre = archivos_variables_nombre

    def extracto_variables(self, variables):
        temp = StringIO()
        indices = self._indices_variables(variables)
        with open(expanduser(self.archivo_datos_nombre), "rt", encoding="utf-8") as f:
            lector = csv.reader(f, skipinitialspace=True)
            for registro in lector:
                valores = [valor for i, valor in enumerate(registro) if i in indices]
                temp.write(f"{','.join(valores)}\n")
        temp.seek(0)

        df = pd.read_csv(temp)
        self._conversion_fechas(variables, df)
        return df
    
    def _indices_variables(self, variables):
        df = pd.read_csv(self.archivo_variables_nombre, names=["Nombre", "Tipo", "Significado"])
        interes = df[df["Nombre"].isin(variables)].index
        return interes.to_list()
    
    def _conversion_fechas(self, variables, df):
        for variable in variables:
            if "fecha" in variable.lower():
                df[variable] = df[variable].apply(self._conversion_fecha) 
    
    @staticmethod
    def _conversion_fecha(fecha_cadena):
        res = fecha_cadena
        if isinstance(fecha_cadena, str):
            c = fecha_cadena.split("/")
            if len(c) < 3:
                print(fecha_cadena)
            else:
                res = date(int(c[2]), int(c[0]), int(c[1]))

        return res