import pandas as pd
from src.extract_data import extract_load as el
from src.plot import PCA
from src.plot import histogram as histplot
import matplotlib.pyplot as plt
import matplotlib.markers as markers
import matplotlib._color_data as mcd
import os

PROTEOMICS = os.path.abspath(os.path.join('..', 'data', 'Protein export list.csv'))
GCMS = os.path.abspath(os.path.join('..', 'data', 'GCMS'))
FTIR_DATA = os.path.abspath(os.path.join('..', 'data', 'Cold FTIR.csv'))

class DataAnalyser():
    def __init__(self):
        self.log2=True

    def plot_PCA_scores(self, data_name, pca_object, explained_variance, labels):

        myplt=plt.subplot(111)
        plt.title('{} PCA scores plot'.format(data_name))
        myplt.set_xlabel('PC1 {}%'.format(round(explained_variance[0]*100 ,2)))
        myplt.set_ylabel('PC2 {}%'.format(round(explained_variance[1]*100 ,2)))

        box = myplt.get_position()
        myplt.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])

        colourlist = [name for name in mcd.CSS4_COLORS][9:]
        markerlist= list(markers.MarkerStyle.markers.keys())

        data =pd.DataFrame(pca_object, index=labels)
        for number, item in enumerate(pd.unique(labels)):
            data_subset=data.loc[item]
            myplt.scatter(data_subset.iloc[:,0], data_subset.iloc[:,1], c=colourlist[number], marker=markerlist[number], label=item)

        plt.legend(fontsize='x-small', loc='upper left', bbox_to_anchor=(1, 1))



    def plot_PCA_loadings(self, data_name, pca_loadings, explained_variance, value_labels, write_loadings=False):
        #%TODO make this work with axis labels
        if write_loadings:
            data=pd.DataFrame(data=pca_loadings,columns=value_labels)
            data=data.transpose()
            if self.log2:
                data.to_csv('..\data\complete\{}_PCA_loadings_log2.csv'.format(data_name))
            else:
                data.to_csv('..\data\complete\{}_PCA_loadings.csv'.format(data_name))

        myplt1 = plt.subplot(111)

        for i, label in enumerate(value_labels):
            myplt.text(pca_loadings[0, i], pca_loadings[1, i], label)

        #plt.scatter(pca_loadings[0, :], pca_loadings[1, :],s=0.5)
        #myplt1.title('{} PCA loadings plot'.format(data_name))
        #myplt1.set_xlabel('PC1 {}%'.format(round(explained_variance[0]*100 ,2)))
        #myplt1.set_ylabel('PC2 {}%'.format(round(explained_variance[1]*100 ,2)))
        myplt1.xlim([min(pca_loadings[0]),max(pca_loadings[0])])
        myplt1.ylim([min(pca_loadings[1]), max(pca_loadings[1])])

    def main(self):
        self.log2=True
        path = GCMS
        clean_data = el.transform_to_dataframe(path)
        PCAprocessor = PCA.PCAtransformer(clean_data, log2 = self.log2)


        #histplot.plot_histogram(clean_data)
        #PCAprocessor.find_optimal_PCs(clean_data)
        scores, loadings, explained_variance = PCAprocessor.calculate_PCA(log2=self.log2)
        #self.plot_PCA_scores(os.path.basename(path), scores, explained_variance, PCAprocessor.get_sample_samplelabels_for_PCA())
        self.plot_PCA_loadings(os.path.basename(path), loadings, explained_variance, PCAprocessor.get_value_labels(), write_loadings=False)
        plt.show()






if __name__ == '__main__':
    data=DataAnalyser()
    data.main()