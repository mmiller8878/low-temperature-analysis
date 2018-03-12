import pandas as pd
import codecs
import os
COLUMNS=['WT Cntl 1','WT Cntl 2','WT Cntl 3','WT Cntl 4','WT cold 1','WT cold 2','WT cold 3','WT cold 4','fum2 Cntl 1','fum2 Cntl 2','fum2 Cntl 3','fum2 Cntl 4','fum2 Cold 1','fum2 Cold 2','fum2 Cold 3','fum2 Cold 4']


def check_file_exists(filepath):
    '''checks file exists in directory and raises exception to the function that called it if there is a problem'''
    try:
        file = open(filepath)
        file.close()
    except (IOError,FileNotFoundError):
        print('file not found')
        raise


def transform_to_dataframe(path):
    if 'Protein export list' in path:
        data = pd.read_csv(path)
        clean_data=pd.DataFrame(data.iloc[0:2427,0])
        clean_data['Name']=data['Description']
        cols = clean_data.columns
        clean_data = clean_data[['Accession']]
        clean_data.rename({'Accession':'labels'}, axis='columns')
        clean_data[COLUMNS]=data.loc[:,'WT Cntl 1':'fum2 Cold 4']
        clean_data[COLUMNS] = clean_data[COLUMNS].apply(pd.to_numeric)
        return  clean_data

    else:
        clean_data=pd.DataFrame()
        for filename in os.listdir(path):
            if 'Cold Day' in filename or 'Control day' in filename:
                data=pd.read_excel(path + filename)
                data = data.iloc[1:,4:]
                data=data[pd.notnull(data.iloc[:,0]) ]
                data=data[data.iloc[:,0].str.contains('Unknown') == False]
                DATA_COLS = [0,2,6,10,14,18]
                data=data.iloc[:,[0,2,6,10,14,18]]
                COLNAMES=['Compound', '{} 1', '{} 2', '{} 3', '{} 4', '{} 5']
                COLNAMES=[col.format(filename.rsplit('.xlsx')[1]) for col in COLNAMES]
                print(data)






