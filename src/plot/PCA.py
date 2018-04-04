import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale

class PCAtransformer():
    '''
    input dataframe has to be a dataframe with sample labels as columns and intensity labels as an index
    '''
    def __init__(self, dataframe, log2):
        self.raw_DF = dataframe

        self.samplelabels=list(self.raw_DF.columns[1:])
        self.samplelabels_for_PCA=self._sample_no_removed(self.samplelabels)
        self.valuelabels=list(self.raw_DF.index)
        self.processed_DF = None

        if self.processed_DF == None:
            self.processed_DF = self.raw_DF.iloc[:, 1:]
            self.processed_DF=self.processed_DF.transpose()
            self.processed_DF.reset_index(inplace=True,drop=True)


        self.PCA_object = self._calculate_PCA_with_10_PCs(log2=log2)




    def _sample_no_removed(self, label_list):
        sample = []
        for i in label_list:
            i = i[:-1]
            sample.append(i)
        return sample

    def _calculate_PCA_with_10_PCs(self, log2):
        pca = PCA(n_components=10)
        if log2:
            self.processed_DF = np.log2(self.processed_DF)
        return pca.fit(self.processed_DF)

    def find_optimal_PCs(self, dataframe):
        '''Run before PCA - shows plot of PCs so optimal number can be chosen'''
        #this line converts values to cumulative PCs as percentages so they can be plotted
        show_cumulative_PCs = np.cumsum(np.round(self.PCA_object.explained_variance_ratio_, decimals=4) * 100)

        plt.clf()
        plt.plot(show_cumulative_PCs)
        plt.show()


    def calculate_PCA(self, log2=False):
        '''returns a dictionary containing the PCA scores and loadings which can be plotted however you want, in main'''

        try:
            scores = self.PCA_object.transform(self.processed_DF)
            loadings = self.PCA_object.components_
            explained_variance = self.PCA_object.explained_variance_ratio_
            results = scores, loadings, explained_variance
        except:
            raise
        return results

    def get_sample_samplelabels_for_PCA(self):
        return self.samplelabels_for_PCA

    def get_value_labels(self):
        return self.valuelabels

