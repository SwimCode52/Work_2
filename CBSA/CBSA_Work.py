import pandas as pd


CBSA_Titles= pd.read_csv('/Users/loganlaberge/Work_2/CBSA/CBSA_Title.csv', dtype={'CBSA Code':"string"})


ZIP_CBSA = pd.read_csv("/Users/loganlaberge/Work_2/CBSA/ZIP_CBSA.csv", dtype={'ZIP':"string", "CBSA":"string"})


CBSA_columns=['CBSA Code', 'CBSA Title']


Titles=CBSA_Titles[CBSA_columns]
Titles=Titles.rename(columns={'CBSA Code':'CBSA'})


ZIP_column=['ZIP', 'CBSA']


ZIP=ZIP_CBSA[ZIP_column]


Combined=pd.merge(ZIP,Titles, on='CBSA')


Combined_nodup=Combined.drop_duplicates(subset=['ZIP', 'CBSA'])


def split_states(df, column_name):
    # Extract state information (assumes states are always at the end)
    df.loc[:, 'State'] = df[column_name].str.extract(r'([A-Z]{2}(?:-[A-Z]{2})*)$')[0]
    

    # Split hyphenated states into a list (e.g., "NY-NJ" becomes ["NY", "NJ"])
    df['State'] = df['State'].str.split('-')
    
    # Expand the lists into separate rows
    df = df.explode('State', ignore_index=True)

    return df





Combined_nodup_new=split_states(Combined_nodup, 'CBSA Title')

Combined_nodup_new


Combined_nodup_new.to_csv('ZIP_CBSA_Combined.csv', index=False)


