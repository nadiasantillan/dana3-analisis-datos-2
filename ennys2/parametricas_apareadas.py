from pandas import DataFrame
# import logging
from normalidad import AnalisisNormalidad
from prettytable import PrettyTable    
from seaborn import barplot
import matplotlib.pyplot as plt
class IMCMujeresAdultas:
    def __init__(self, configuracion, df: DataFrame):
        self.configuracion = configuracion
        self.variable = "IMC"
        self.df = df[(df["años_cumplidos"]>=20)&(df["antropo_sex"]=="mujer")&(df[self.variable].notna())]
        self.prevalencias2005 = DataFrame(data = [
            ["Centro", "20 a 30 años", 0.344],
            ["Centro", "30 a 40 años", 0.452],
            ["Centro", "40 a 50 años", 0.643],
            ["GBA", "20 a 30 años", 0.324],  
            ["GBA", "30 a 40 años", 0.459],
            ["GBA", "40 a 50 años", 0.58],
            ["Cuyo", "20 a 30 años", 0.302],
            ["Cuyo", "30 a 40 años", 0.357],
            ["Cuyo", "40 a 50 años",  0.615],
            ["NEA", "20 a 30 años", 0.228],
            ["NEA", "30 a 40 años", 0.430],
            ["NEA", "40 a 50 años", 0.701],
            ["NOA", "20 a 30 años", 0.375],
            ["NOA", "30 a 40 años", 0.509],
            ["NOA", "40 a 50 años", 0.632],
            ["Patagonia", "20 a 30 años", 0.375],
            ["Patagonia", "30 a 40 años", 0.509],
            ["Patagonia", "40 a 50 años",  0.632]], columns=("Región", "Rango Etario", "Prevalencia"))

        
    def analisis(self):
        tabla = PrettyTable()
        tabla.field_names = ["Región", "20 a 30", "30 a 40", "40 a 50"]
        rangos_etareos = [(20,30), (30, 40), (40, 50)]
        data = []
        
        for region in ["Centro", "GBA", "Cuyo", "NEA", "NOA", "Patagonia"]:
            fila_region = [region]
            # p = AnalisisNormalidad(
            #     self.df[(self.df["region"]==region)], 
            #     self.variable, 
            #     f"{self.variable} mujeres entre 20 y 49 años - Región {region}")
            # _, df_sin_atipicos = p.analisis()
            # p.graficos()
            for edad_desde, edad_hasta in rangos_etareos:
                p = AnalisisNormalidad(self.configuracion,
                    self.df[(self.df["region"]==region)&(self.df["años_cumplidos"]>=edad_desde)&(self.df["años_cumplidos"]<edad_hasta)], 
                    self.variable, 
                    f"{self.variable} mujeres entre {edad_desde} y {edad_hasta} años - Región {region}")
                _, df_sin_atipicos = p.analisis()
                p.graficos()
                prevalencia = round(len(df_sin_atipicos[(df_sin_atipicos[self.variable]>25)])/len(df_sin_atipicos),3)
                fila_region.append(
                    round(len(df_sin_atipicos[(df_sin_atipicos[self.variable]>25)])/len(df_sin_atipicos),3))
                data.append((2018, region, f"{edad_desde} a {edad_hasta} años", prevalencia))
            tabla.add_row(fila_region)
        print(tabla)
        df = DataFrame(data, columns=("Encuesta", "Región", "Rango Etario", "Prevalencia"))
        directorio = self.configuracion.as_dict()["salida"]["directorio"]
        df.to_csv(f"{directorio}/sobrepeso_2018.csv", index=False)
        plt.clf()
        fig, (ax11, ax21) = plt.subplots(1, 2, figsize=(10, 6))
        barplot(self.prevalencias2005, x="Región", hue="Rango Etario", y="Prevalencia", ax=ax11)
        ax11.set_ylim([0, 0.9])
        ax11.set_title("2005")
        barplot(df, x="Región", hue="Rango Etario", y="Prevalencia", ax=ax21)
        ax21.set_ylim([0, 0.9])
        ax21.set_title("2018")
        fig.suptitle("Comparación Prevalencia de Sobrepeso en Mujeres entre 20 y 49 años")
        plt.savefig(f"{directorio}/prevalencias_2018.png")
        plt.close()

        