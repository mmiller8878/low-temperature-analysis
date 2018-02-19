import pandas as pd
COLUMNS=['WT Cntl 1','WT Cntl 2','WT Cntl 3','WT Cntl 4','WT cold 1','WT cold 2','WT cold 3','WT cold 4','fum2 Cntl 1','fum2 Cntl 2','fum2 Cntl 3','fum2 Cntl 4','fum2 Cold 1','fum2 Cold 2','fum2 Cold 3','fum2 Cold 4']


def check_file_exists(filepath):
    '''checks file exists in directory and raises exception to the function that called it if there is a problem'''
    try:
        file = open(filepath)
        file.close()
    except (IOError,FileNotFoundError):
        print('file not found')
        raise


def transform_to_dataframe(file):
    data=pd.read_csv(file)
    if 'Protein export list' in file:
        clean_data=pd.DataFrame(data.iloc[0:2427,0])
        clean_data['Name']=data['Description']
        cols = clean_data.columns
        clean_data = clean_data[['Accession']]
        clean_data.rename({'Accession':'labels'}, axis='columns')
        clean_data[COLUMNS]=data.loc[:,'WT Cntl 1':'fum2 Cold 4']
        clean_data[COLUMNS] = clean_data[COLUMNS].apply(pd.to_numeric)
        return  clean_data


