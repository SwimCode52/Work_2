import pandas as pd


CBSA_Titles= pd.read_csv('/Users/loganlaberge/Documents/Work/Mailing_List/CBSA_Work/ZIP_CBSA/CBSA_Title.csv', dtype={'CBSA Code':"string"})


ZIP_CBSA = pd.read_csv("/Users/loganlaberge/Documents/Work/Mailing_List/CBSA_Work/ZIP_CBSA/ZIP_CBSA.csv", dtype={'ZIP':"string", "CBSA":"string"})


CBSA_columns=['CBSA Code', 'CBSA Title']


Titles=CBSA_Titles[CBSA_columns]
Titles=Titles.rename(columns={'CBSA Code':'CBSA'})


ZIP_column=['ZIP', 'CBSA']


ZIP=ZIP_CBSA[ZIP_column]


Combined=pd.merge(ZIP,Titles, on='CBSA')


Combined_nodup=Combined.drop_duplicates(subset=['ZIP', 'CBSA'])


def split_states(df, column_name):
   # Extract state information (assuming it's always at the end of the string)
   df['State'] = df[column_name].str.extract(r'([A-Z]{2}(?:-[A-Z]{2})*)$')[0]


   # Split hyphenated states and expand into separate rows
   df = df.assign(State=df['State'].str.split('-')).explode('State', ignore_index=True)


   return df


split_states(Combined_nodup, 'CBSA Title')




Combined_nodup.to_csv('ZIP_CBSA_Combined.csv', index=False)


