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
        clean_data.set_index(keys='Accession', drop=True, inplace=True)
        return  clean_data

    else:
        counter=0
        merged=pd.DataFrame()
        for filename in os.listdir(path):
            print(filename)
            if 'Cold Day' in filename or 'Control day' in filename:
                if '~$' in filename:
                    continue
                data=pd.read_excel(path + '/' + filename, index_col=None)

                data.reset_index(inplace=True)

                data =  data[~data.apply(lambda row: row.astype(str).str.contains('Area', case=False).any(), axis=1)]

                data = data.iloc[:, [0,4,5,6,7,8]]

                data=data[pd.notnull(data.iloc[:,0]) ]
                data=data[data.iloc[:,0].str.contains('Unknown') == False]

                COLNAMES=['Compound','{} 1', '{} 2', '{} 3', '{} 4', '{} 5']
                COLNAMES=[col.format(filename.split('.xlsx')[0]) for col in COLNAMES]
                data.columns=COLNAMES
                data.set_index(keys='Compound', drop=True, inplace=True)
                newindex=pd.Series([data.split('_')[0] for data in data.index.values])
                data.set_index(keys=newindex, drop = True, inplace = True)
                data = data.groupby(data.index).sum()
                data.replace(int(0), int(1), inplace=True)
                merged = data if counter is 0 else pd.merge(data, merged, left_index=True, right_index=True)
                counter+=1

        return merged







