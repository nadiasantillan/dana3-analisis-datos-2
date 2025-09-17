from herramientas.lector import Lector
from herramientas.fechas import edad, edad_meses
from herramientas.subsets import TablaConVariable
import logging
import os
import pandas as pd

class Tablas:
    def __init__(self, archivo_encuesta, archivo_alimentos, archivo_nutrientes, configuracion):
        self.archivo_encuesta = archivo_encuesta
        self.archivo_alimentos = archivo_alimentos
        self.archivo_nutrientes = archivo_nutrientes
        self.configuracion = configuracion.as_dict()
        
        self._encuesta = self._tabla_encuesta()
        _nutrientes = self._tabla_nutrientes()
        _alimentos = self._tabla_alimentos()
        
        self._nutrientes = pd.merge(self._encuesta, _nutrientes, on="miembro_id", how="inner")
        self._alimentos = pd.merge(self._encuesta, _alimentos, on="miembro_id", how="inner")
        
    def tabla_encuesta(self):
        return self._encuesta
    
    def tabla_alimentos(self):
        return self._alimentos
    
    def tabla_nutrientes(self):
        return self._nutrientes
    
    def _tabla_encuesta(self):
        logging.info("[%s] Carga base de datos encuesta iniciada",
                     self.__class__.__name__)
        l = Lector(self.archivo_encuesta)
        df = l.extracto_variables(self.configuracion["encuesta"]["variables"], variables_fecha=self.configuracion["encuesta"]["variables_fecha"])
        df["años_cumplidos"] = df.apply(lambda fila: edad(fila["antropo_fnac"], fila["fecha_entr"]), axis=1)
        df["meses_cumplidos"] = df.apply(lambda fila: edad_meses(fila["antropo_fnac"], fila["fecha_entr"]), axis=1)
        logging.info("[%s] Carga base de datos encuesta finalizada: %d registros",
                     self.__class__.__name__,
                     len(df))
        return df

    def _tabla_nutrientes(self):
        logging.info("[%s] Carga base de datos nutrientes iniciada",
                     self.__class__.__name__)
        l = Lector(self.archivo_nutrientes)
        df = l.extracto_variables(self.configuracion["nutrientes"]["variables"], variables_fecha=self.configuracion["nutrientes"]["variables_fecha"])
        logging.info("[%s] Carga base de datos nutrientes finalizada: %d registros",
                     self.__class__.__name__,
                     len(df))
        return df
    
    def _tabla_alimentos(self):
        logging.info("[%s] Carga base de datos alimentos iniciada",
                     self.__class__.__name__)
        variables_extra = []
        c = self.configuracion["alimentos"]
        if c["archivo_variables"]:
            t = TablaConVariable(c["archivo_variables"]["archivo_nombre"],c["archivo_variables"]["variable_variable"],c["archivo_variables"]["variable_condicion"], delimitador="|")
            variables_extra = t.variables()
        l = Lector(self.archivo_alimentos)
        df = l.extracto_variables(c["variables"]+variables_extra, variables_fecha=c["variables_fecha"])
        logging.info("[%s] Carga base de datos alimentos finalizada: %d registros",
                     self.__class__.__name__,
                     len(df))
        return df
    
    def archivos(self):
        directorio = self.configuracion["salida"]["directorio"]
        if not os.path.exists(directorio):
            os.makedirs(directorio)
        logging.info("[%s] Guardando tablas en %s", self.__class__.__name__, self.configuracion["salida"]["directorio"])
        self.tabla_encuesta().to_csv(f"{directorio}/encuesta.csv", index=False)
        self.tabla_alimentos().to_csv(f"{directorio}/alimentos.csv", index=False)