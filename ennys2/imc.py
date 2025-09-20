import logging
from pandas import DataFrame, read_csv
from prettytable import PrettyTable
from constantes import REGIONES, RANGOS_ETARIOS_MUJERES
from seaborn import heatmap
import matplotlib.pyplot as plt
from herramientas.configuracion import Configuracion

class IMC:
    def __init__(self, df: DataFrame, config: Configuracion):
        self.df = df[(df["antropo_sex"]=="mujer")&(df["E_CUEST"]=="18 o mas años")&(df["años_cumplidos"]>=20)]
        self.variables = ["IMC", "IMC2", "imc_calculado", "PESO", "PESO2", "TALLA", "TALLA2"]
        self.df["imc_calculado"] = self.df["PESO2"]/((self.df["TALLA2"]/100)**2)
        config_dict = config.as_dict()
        self.df_2005 = read_csv(config_dict["ennys1"]["prevalencia_sobrepeso_mujeres"])
        logging.info("Mujeres de 18 o más años %d", len(self.df))
        
    def analisis(self):
        tabla = PrettyTable(("Variable", "Cantidad", "Cantidad nulos", "Media", "Mediana", "Desvio"))
        registros = len(self.df)
        for variable in self.variables:
            faltantes = len(self.df[self.df[variable].isna()])
            tabla.add_row((variable, registros, faltantes, self.df[variable].mean(), self.df[variable].median(), self.df[variable].std()))
            
        logging.info("\n%s", tabla)
        
    def graficos(self):
        df = self._resumen_ennys2()
        plt.clf()
        figure, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))
        self._heatmap(df, ax1, "Prevalencia sobrepeso", "IMC > 25")
        self._heatmap(df, ax2, "Prevalencia obesidad", "IMC > 30")
        self._heatmap(df, ax3, "Prevalencia obesidad mórbida", "IMC > 40")
        figure.suptitle("Prevalencia de IMC Alto en Mujeres - ENNyS 2018")
        plt.show()
        
        plt.clf()        
        figure, ax1 = plt.subplots(1, 1, figsize=(6, 5))
        self._heatmap(self.df_2005, ax1, "Prevalencia", "IMC > 25")
        figure.suptitle("Prevalencia de IMC Alto en Mujeres - ENNyS 2005")
        plt.show()
        
    def _heatmap(self, df, ax, value, titulo):
        hm = df.pivot(index="region", columns="Rango etario", values=value)
        heatmap(hm, annot=True, cmap="crest", ax=ax)
        ax.set_title(titulo)
        ax.set_ylabel("Región")
        
    def _resumen_ennys2(self):
        for edad_min, edad_max, nombre in RANGOS_ETARIOS_MUJERES:
            self.df.loc[(self.df["años_cumplidos"]>= edad_min)&(self.df["años_cumplidos"]< edad_max), "Rango etario"] = nombre
        self.df["categoria_imc"] = ""
        self.df.loc[(self.df["IMC2"]>25), "categoria_imc"] = "Sobrepeso"
        self.df.loc[(self.df["IMC2"]>30), "categoria_imc"] = "Obesidad"
        self.df.loc[(self.df["IMC2"]>40), "categoria_imc"] = "Obesidad mórbida"
        
        data = []
        for region in REGIONES:
            for _, _, rango_nombre in RANGOS_ETARIOS_MUJERES:
                sobrepeso = len(self.df[(self.df["categoria_imc"].isin(("Sobrepeso", "Obesidad", "Obesidad mórbida")))&(self.df["Rango etario"]==rango_nombre)&(self.df["region"]==region)])
                obesidad = len(self.df[(self.df["categoria_imc"].isin(("Obesidad", "Obesidad mórbida")))&(self.df["Rango etario"]==rango_nombre)&(self.df["region"]==region)])
                obesidad_morbida = len(self.df[(self.df["categoria_imc"]=="Obesidad mórbida")&(self.df["Rango etario"]==rango_nombre)&(self.df["region"]==region)])
                total = len(self.df[(self.df["Rango etario"]==rango_nombre)&(self.df["region"]==region)]) 
                data.append((
                    region, 
                    rango_nombre, 
                    sobrepeso,
                    total,
                    sobrepeso/total,
                    obesidad/total,
                    obesidad_morbida/total))
                
        return DataFrame(data, columns=("region", "Rango etario", "Cantidad Sobrepeso", "Cantidad total", "Prevalencia sobrepeso", "Prevalencia obesidad", "Prevalencia obesidad mórbida"))

        
            