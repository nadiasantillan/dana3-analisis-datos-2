from scipy.stats import norm
import numpy as np

class Normal:
    def __init__(self, media, desvio):
        self.media = media
        self.desvio = desvio
        
    def x(self, n = 1000):
        t = self._teorica()
        return np.linspace(t.ppf(0.01), t.ppf(0.99), n)
    
    def y(self):
        t = self._teorica()
        return t.pdf(self.x())
    
    def _teorica(self):
        return norm(self.media, self.desvio)
        