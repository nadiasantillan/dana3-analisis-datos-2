import pandas as pd
import matplotlib.pyplot as plt
from normalidad import AnalisisNormalidad
from noparametricas import MannWhitneyU

class AlimentosUltraprocesados:
    def __init__(self, configuracion):
        self.configuracion = configuracion.as_dict()
        self.columnas = self.configuracion["alimentos"]["archivo_variables"]["variables"]
        self.categoria_bebidas = self.configuracion["alimentos"]["archivo_variables"]["categoria_bebidas"]
        self.variable_condicion = self.configuracion["alimentos"]["archivo_variables"]["variable_condicion"]
        self.variable_nombre = self.configuracion["alimentos"]["archivo_variables"]["variable_variable"]
        self.variables = self._variables(self.configuracion["alimentos"]["archivo_variables"]["archivo_nombre"]) 
        
    def markdown_variables(self):
        res = "|"+"|".join(self.columnas) + "|\n"
        res += "|"+"|".join(["-------" for _ in self.columnas]) + "|\n"
        for _, row in self.variables[self.columnas].iterrows():
            res += "|" + "|".join([row[nombre] for nombre in self.columnas])  + "|\n"
        return res 
    
    def _variables(self, nombre_archivo):
        df = pd.read_csv(nombre_archivo, sep="|")
        return df[df[self.variable_condicion].notna()]
    
    def variables_para(self, categoria):
        return self.variables[self.variables[self.variable_condicion]==categoria]
    
    def tabla_alimentos_categoria(self, alimentos, categoria):
        variables = self.variables[self.variables[self.variable_condicion]==categoria][self.variable_nombre].to_list()
        variables_en_alimentos = [variable for variable in variables if variable in alimentos.columns]
        df = alimentos[self.configuracion["alimentos"]["variables"] + ["años_cumplidos", "antropo_sex"]+ variables_en_alimentos]
        variable_total = f"Total {categoria}"
        df[variable_total] = df[variables_en_alimentos].sum(axis = 1)
        
        return df
        
    def analisis(self, alimentos):
        print(alimentos.head())
        for categoria in ["Bebidas azucaradas", "Galletitas", "Pasteleria", "Copetin", "Golosinas", "Comida Rápida"]:
           df = self.tabla_alimentos_categoria(alimentos, categoria)
           significativa, mujeres, varones = self.analisis_categoria(df, categoria) 
           if significativa:
               self.grafico_diferencia_significativa(categoria, mujeres, varones)
        
    def analisis_categoria(self, consumo, categoria):        
        mujeres_adultas = consumo[(consumo["años_cumplidos"]>=18)&(consumo["años_cumplidos"]<50)&(consumo["antropo_sex"]=="mujer")] 
        varones_adultos = consumo[(consumo["años_cumplidos"]>=18)&(consumo["años_cumplidos"]<50)&(consumo["antropo_sex"]=="varón")]
        res = MannWhitneyU(mujeres_adultas, varones_adultos, f"Total {categoria}", f"Consumo en gramos de {categoria} - Mujeres vs varones adultos").test()
        return res.pvalue < 0.01, mujeres_adultas, varones_adultos
        
    def grafico_diferencia_significativa(self, categoria, mujeres, varones):
        directorio = self.configuracion["salida"]["directorio"]
        titulo = f"Consumo de {categoria} en Adultos"
        plt.clf()
        fig, (ax11, ax21) = plt.subplots(1, 2, figsize=(10, 6))
        fig.suptitle(titulo)

        ax11.set_ylim([0, 4700])
        ax21.set_ylim([0, 4700])
        ax11.hist(mujeres[f"Total {categoria}"], bins=[0, 500, 1000, 1500, 2000, 2500, 3000], edgecolor="black", facecolor="pink") 
        ax21.hist(varones[f"Total {categoria}"], bins=[0, 500, 1000, 1500, 2000, 2500, 3000], edgecolor="black") 

        ax11.set_xlabel("Cantidad (g)")
        ax11.set_ylabel("Mujeres")
        ax21.set_xlabel("Cantidad (g)")
        ax21.set_ylabel("Varones")        

        archivo_nombre = titulo.replace(" ", "_")
        plt.savefig(f"{directorio}/{archivo_nombre}.png")
        plt.close()
    