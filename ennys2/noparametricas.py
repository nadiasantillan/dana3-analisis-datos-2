import logging
from scipy.stats import mannwhitneyu

class MannWhitneyU:
    def __init__(self, df1, df2, variable, titulo):
        self.df1 = df1
        self.df2 = df2
        self.variable = variable
        self.titulo = titulo
    
    def test(self):
        logging.info("[%s] Medianas %s: %.3f %.3f",
                     self.__class__.__name__,
                     self.titulo,
                     self.df1[self.variable].median(),
                     self.df2[self.variable].median())
        res = mannwhitneyu(self.df1[self.variable], self.df2[self.variable], alternative="less")
        logging.info("test %s", res)
        return res
        
        