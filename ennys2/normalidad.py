from pandas.core.series import Series
from pandas import DataFrame
from scipy.stats import normaltest, norm, kstest
import logging
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from distribuciones import Normal

class PruebaNormalidad:
    def __init__(self, series: Series):
        self.series = series
        
    def es_normal(self):
        return self._dagostino_pearson() or self._kolmorogov_smirnov()
    
    def _dagostino_pearson(self):
        res = normaltest(self.series)
        logging.info(
            "[%s] D’Agostino and Pearson’s p-value=%s", 
            self.__class__.__name__, 
            res.pvalue)
        return res.pvalue > 0.01
    
    def _kolmorogov_smirnov(self):
        rng = np.random.default_rng()
        media = self.series.mean()
        desvio = self.series.std()
        teorica = norm(loc=media, scale=desvio)
        x = teorica.rvs(size=5000, random_state=rng)
        res = kstest(self.series, teorica.cdf)
        logging.info(
            "[%s] Kolmorogov-Smirnov p-value=%s", 
            self.__class__.__name__, 
            res.pvalue)
        return res.pvalue > 0.01
    
class AnalisisNormalidad:
    def __init__(self, configuracion, df: DataFrame, variable: str, titulo: str):
        self.configuracion = configuracion.as_dict()
        self.df = df
        self.titulo = titulo
        self.variable = variable
        self.q1, self.q3 = self.df[variable].quantile((.25, .75))
        self.iqr = self.q3 - self.q1
        self.min = self.df[variable].min()
        self.max = self.df[variable].max()
        self.media = self.df[variable].mean()
        self.mediana = self.df[variable].median()
        self.std = self.df[variable].std()        
        self.l1_atipicos = self.q1 - self.iqr
        self.l2_atipicos = self.q3 + self.iqr
        self.df_sin_atipicos = self.df[(self.df[variable] >= self.l1_atipicos)&(self.df[variable] <= self.l2_atipicos)]

    def analisis(self):
        logging.info("[%s] %s: %d, sin valores atípicos: %d",
                     self.__class__.__name__,
                     self.titulo,
                     len(self.df),
                     len(self.df_sin_atipicos))
        logging.info("[%s] %s (media=%.2f, std=%.2f, min=%.2f, max=%.2f, Q1=%.2f, Q3=%.2f, IQR=%.2f, Q1 - 1.5 IQR=%.2f, Q3 + 1.5 IQR=%.2f)",
                     self.__class__.__name__,
                     self.titulo,
                     self.media, 
                     self.std,
                     self.min,
                     self.max,
                     self.q1,
                     self.q3,
                     self.iqr,
                     self.l1_atipicos,
                     self.l2_atipicos)
        normal = PruebaNormalidad(self.df[self.variable]).es_normal()
        self._funcion_log(logging.info, logging.warning, normal)("[%s] Normalidad %s: %s", 
                     self.__class__.__name__,
                     self.titulo,
                     "Si" if normal else "No")
        
        normal_sin_atipicos = PruebaNormalidad(self.df_sin_atipicos[self.variable]).es_normal()
        self._funcion_log(logging.info, logging.error, normal_sin_atipicos)("[%s] Normalidad %s sin valores atípicos: %s", 
                     self.__class__.__name__,
                     self.titulo,
                     "Si" if normal_sin_atipicos else "No")
        return (normal_sin_atipicos, self.df_sin_atipicos)

    def graficos(self):
        directorio = self.configuracion["salida"]["directorio"]
        plt.clf()
        teorica = Normal(self.mediana, self.std)
        # bins = [i*2.5+10 for i in range(30) if i*2.5+10 <=70]
        fig, (ax11, ax21) = plt.subplots(1, 2, figsize=(10, 6))
        fig.suptitle(self.titulo)
        plt.subplots_adjust(wspace=.5, left=0.1, right=0.9)
        bins=20
        
        ax12 = ax11.twinx()
        ax22 = ax21.twinx()

        self._grafico_serie(self.df[self.variable], ax11, ax12, bins, teorica)
        self._grafico_serie(self.df_sin_atipicos[self.variable], ax21, ax22, bins, teorica, sufijo_serie="sin valores atípicos")
        sufijo = self.titulo.replace(" ","_")
        plt.savefig(f"{directorio}/histograma_{sufijo}.png")
        plt.close()
        
    def _grafico_serie(self, serie, ax1, ax2, bins, teorica, sufijo_serie=""):
        sns.histplot(x=serie, ax=ax1, bins=bins)
        ax1.set_xlabel(f"{self.variable} {sufijo_serie}")
        ax1.set_ylabel("Frecuencia")
        sns.lineplot(x=teorica.x(), y=teorica.y(), ax=ax2)

    def _funcion_log(self, fn1, fn2, prueba):
        return fn1 if prueba else fn2