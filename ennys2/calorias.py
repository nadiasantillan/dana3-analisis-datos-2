from constantes import REGIONES
import matplotlib.pyplot as plt
import logging
import pandas as pd
from scipy.stats import binomtest, wilcoxon
from distribuciones import Normal
import seaborn as sns

class ConsumoCaloriasNiños2a5:
    BINS = [i for i in range(250,5000,250)]
    MEDIANAS_2005 = {
        "País": 1560,
        "Centro": 1613,
        "Cuyo": 1563,
        "GBA": 1540,
        "NEA": 1495,
        "NOA": 1456,
        "Patagonia": 1609
    }
    def __init__(self, nutrientes, configuracion):
        self.configuracion = configuracion
        self.subset = nutrientes[(nutrientes["años_cumplidos"]>=2)&(nutrientes["años_cumplidos"]<=5)]
        
    def analisis(self):
        medianas = self._medianas()
        print(medianas)
        self._prueba_signos(medianas)
        self._prueba_wilcoxon(medianas)
        
    def graficos(self):
        directorio = self.configuracion.as_dict()["salida"]["directorio"]
        self._barras_consumo_regiones(directorio)
        
    def _medianas(self):
        mediana_pais = round(self.subset["tot_energia_kcal"].median())
        data = [] #[("País", self.MEDIANAS_2005["País"], mediana_pais)]
        for region in REGIONES:
            df = self.subset[self.subset["region"]==region]
            mediana = round(df["tot_energia_kcal"].median())
            data.append((region, self.MEDIANAS_2005[region], mediana))
        return pd.DataFrame(data, columns=["Región", "2005", "2018"])
            
    def _barras_consumo_regiones(self, directorio):
        plt.clf()
        medianas = self._medianas()
        df = medianas.melt(id_vars=["Región"], var_name="Encuesta", value_name="Ingesta calórica")
        sns.barplot(df, x="Región", y="Ingesta calórica", hue="Encuesta")
        plt.title("Ingesta calórica en niños de 2 a 5 años")
        plt.savefig(f"{directorio}/barras_medianas_ingesta_energetica.png")
        plt.close()        
          
    def _histogramas_consumo_regiones(self, directorio):
        for region in REGIONES:            
            plt.clf()
            sufijo = f"histograma_niños_2_a_5_{region}"
            df = self.subset[self.subset["region"]==region]
            mediana = df["tot_energia_kcal"].median()
            desvio = df["tot_energia_kcal"].std()
            _, ax11 = plt.subplots(1, 1, figsize=(10, 6))
            ax12 = ax11.twinx()
            teorica = Normal(mediana, desvio)
            ax11.hist(df["tot_energia_kcal"], bins=self.BINS, edgecolor="black")
            ax12.plot(teorica.x(), teorica.y(), color="red")
            plt.savefig(f"{directorio}/histograma_{sufijo}.png")
            plt.close()
            
    def _prueba_signos(self, df):
        df["Signo"] = ""
        df.loc[df["2018"] - df["2005"] > 0, "Signo"] = "+"
        df.loc[df["2018"] - df["2005"] < 0, "Signo"] = "-"
        
        n = len(df)
        k = len(df[df["Signo"]=="+"]) 
        res = binomtest(k, n, alternative="less")
        logging.info("[%s] Test de signos: n=%d, k=%d, p-value=%.4f, H0 %s",
                     self.__class__.__name__,
                     n,
                     k,
                     res.pvalue,
                     "se rechaza" if res.pvalue < 0.05 else "no se rechaza")
        
    def _prueba_wilcoxon(self, df):        
        res = wilcoxon(df["2005"], y=df["2018"], alternative="greater")
        logging.info("[%s] Test de wilcoxon: p-valor %.3f, %s",
                     self.__class__.__name__,
                     res.pvalue,
                     "se rechaza" if res.pvalue < 0.05 else "no se rechaza")