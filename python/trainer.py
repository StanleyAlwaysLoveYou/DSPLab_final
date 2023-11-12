from hmmlearn import hmm
import numpy as np
class HMMTrainer(object):
   def __init__(self, model_name='GaussianHMM', n_components=35):
     self.model_name = model_name
     self.n_components = n_components

     self.models = []
     if self.model_name == 'GaussianHMM':
        self.model=hmm.GaussianHMM(self.n_components, n_iter=5000,tol=0, verbose=True)
     else:
        print("Please choose GaussianHMM")
   def train(self, X):
       self.models.append(self.model.fit(X))
   def get_score(self, input_data):
       return self.model.score(input_data)