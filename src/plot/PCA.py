import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale

class PCAtransformer():
    '''
    input dataframe has to be a dataframe with sample labels as columns and intensity labels as an index
    '''
    def __init__(self, dataframe):
        self.raw_DF = dataframe
        self.samplelabels=list(self.raw_DF.columns[1:])
        self.samplelabels_for_PCA=self.sample_no_removed(self.samplelabels)
        self.valuelabels=list(self.raw_DF.iloc[:,0])
        self.processed_DF = None

        if self.processed_DF == None:
            self.processed_DF = self.raw_DF.iloc[:, 1:]
            self.processed_DF=self.processed_DF.transpose()
            self.processed_DF.reset_index(inplace=True,drop=True)




    def sample_no_removed(self, label_list):
        sample = []
        for i in label_list:
            i = i[:-1]
            sample.append(i)
        return sample

    def find_optimal_PCs(self, dataframe):
        '''Run before PCA - shows plot of PCs so optimal number can be chosen'''
        try:
            plt.clf()
            pca = PCA(n_components=10)
            my_PCA = pca.fit(self.processed_DF)
            #this line converts values to cumulative PCs as percentages so they can be plotted
            show_cumulative_PCs = np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4) * 100)

            plt.plot(show_cumulative_PCs)
            plt.show()
        except:
            raise

    def calculate_PCA(self, log2=False):
        '''returns a dictionary containing the PCA scores and loadings which can be plotted however you want, in main'''

        try:
            pca = PCA(n_components=10)
            if log2:
                self.processed_DF = np.log2(self.processed_DF)
            pca.fit(self.processed_DF)
            scores = pca.transform(self.processed_DF)
            loadings = pca.components_
            results = scores, loadings
        except:
            raise
        return results

    def get_sample_samplelabels_for_PCA(self):
        return self.samplelabels_for_PCA

    def get_value_labels(self):
        return self.valuelabels

