import pandas as pd
from src.extract_data import extract_load as el
from src.plot import PCA as pcaplot
from src.plot import histogram as histplot

import matplotlib.pyplot as plt



def load_file(filepath):
    colstouse = [8, 10, 12] + list(range(15, 35))
    datafile = pd.read_csv(filepath, header=1, usecols=colstouse)
    datafile.set_index(['Sequence'],drop=True)
    return datafile

def plot_PCA_scores(pca_object):
    plt.scatter(pca_object[0:5, 0], pca_object[0:5, 1], c='b', marker="v", label='WTLL')
    plt.scatter(pca_object[5:10, 0], pca_object[5:10, 1], c='g', marker=">", label='WTHL')
    plt.scatter(pca_object[10:15, 0], pca_object[10:15, 1], c='r', marker="*", label='gpt2LL')
    plt.scatter(pca_object[15:20, 0], pca_object[15:20, 1], c='y', marker="1", label='gpt2HL')
    plt.legend()
    plt.show()

def plot_PCA_loadings(pca_loadings):
    plt.scatter(pca_loadings[0, :], pca_loadings[1, :],s=0.5)
    plt.xlim([-0.006,0.007])
    plt.ylim([-0.011, 0.011])
    plt.show()

def main():
    try:
        path = '..\data\peptide values proteomics.csv'
        el.check_file_exists(path)
        clean_data = load_file(path)
    except (IOError,FileNotFoundError) as err:
        print('file or directory does not exist')
        print(err.args)

    else:
        #histplot.plot_histogram(clean_data)
        #pcaplot.find_optimal_PCs(clean_data)
        scores = pcaplot.plot_pca_scores(clean_data)['scores']
        loadings = pcaplot.plot_pca_scores(clean_data)['loadings']
        plot_PCA_scores(scores)
        #plot_PCA_loadings(loadings)
        #plt.show()






if __name__ == '__main__':
    main()