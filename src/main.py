import pandas as pd
from src.extract_data import extract_load as el
from src.plot import PCA
from src.plot import histogram as histplot
import matplotlib.pyplot as plt
import matplotlib.markers as markers
import numpy as np

PROTEIN_DATA = '..\data\Protein export list.csv'
RAW_GCMS= '..\\data\\'
GCMS_DATA_FUM2= r'..\data\fum2 GCMS.csv'
FTIR_DATA='..\data\Cold FTIR.csv'

class DataAnalyser():
    def __init__(self):
        self.log2=False

    def plot_PCA_scores(self, pca_object, labels):

        markerlist= list(markers.MarkerStyle.markers.keys())

        data =pd.DataFrame(pca_object, index=labels)
        for number, item in enumerate(pd.unique(labels)):
            data_subset=data.loc[item]
            plt.scatter(data_subset.iloc[:,0], data_subset.iloc[:,1], c='C'+str(number), marker=markerlist[number], label=item)
        plt.legend()



    def plot_PCA_loadings(self, pca_loadings, value_labels, write_loadings=False):

        if write_loadings:
            data=pd.DataFrame(data=pca_loadings,columns=value_labels)
            data=data.transpose()
            if self.log2:
                data.to_csv('..\data\PCA_loadings_log2.csv')
            else:
                data.to_csv('..\data\PCA_loadings.csv')




        for i, label in enumerate(value_labels):
            plt.text(pca_loadings[0, i], pca_loadings[1, i], label)

        #plt.scatter(pca_loadings[0, :], pca_loadings[1, :],s=0.5)
        plt.xlim([min(pca_loadings[0]),max(pca_loadings[0])])
        plt.ylim([min(pca_loadings[1]), max(pca_loadings[1])])

    def main(self):
        self.log2=True
        path = RAW_GCMS
        clean_data = el.transform_to_dataframe(path)
        PCAprocessor = PCA.PCAtransformer(clean_data)


        #histplot.plot_histogram(clean_data)
        PCAprocessor.find_optimal_PCs(clean_data)
        scores, loadings= PCAprocessor.calculate_PCA(log2=self.log2)
        self.plot_PCA_scores(scores, PCAprocessor.get_sample_samplelabels_for_PCA())
        self.plot_PCA_loadings(loadings, PCAprocessor.get_value_labels(), write_loadings=False)
        plt.show()






if __name__ == '__main__':
    data=DataAnalyser()
    data.main()