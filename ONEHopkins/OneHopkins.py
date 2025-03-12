import pandas as pd

giving= pd.read_csv('/Users/loganlaberge/Work_2/ONEHopkins/Giving.csv', dtype={'Hard and Soft Credit : Constituent : JHAS ID':'string'})

giving=giving.rename(columns={'Hard and Soft Credit : Constituent : JHAS ID':'JHAS ID'})

recent = pd.read_csv('/Users/loganlaberge/Work_2/ONEHopkins/MostRecent.csv', dtype={'Hard and Soft Credit : Constituent : JHAS ID':'string'})

recent.columns
recent= recent.rename(columns={'Hard and Soft Credit : Constituent : JHAS ID':'JHAS ID',
                               'Hard and Soft Credit : Constituent : Date of Most Recent Gift': 'Most Recent Gift',
       'Hard and Soft Credit : Constituent : Date of Most Recent Pledge':'Most Recent Pledge'})

# merge=pd.merge(giving,recent, on='JHAS ID')

giving_jhasgrouped_df = giving.groupby(['JHAS ID', 'Fiscal Years']).agg({
    'Credit Amount': 'sum'
}).reset_index()

giving_jhasgrouped_df



giving_pivot = giving_jhasgrouped_df.pivot(index='JHAS ID', 
                                           columns='Fiscal Years', 
                                           values='Credit Amount').fillna(0).reset_index()
giving_pivot.columns.name = None  # Remove the 'Fiscal Years' name
giving_pivot = giving_pivot.reset_index()  # Ensure JHAS ID is a column


giving.dtypes
merged=pd.merge(giving_pivot,recent,on='JHAS ID')

merge=merged.drop_duplicates()

#Bring in the lists
donors=pd.read_csv('/Users/loganlaberge/Work_2/ONEHopkins/Donors.csv', dtype={'JHAS ID':'string'})

donors_dedup=donors.drop_duplicates(subset=['JHAS ID'])
donors_dedup

donors_dedup

merged_donors=pd.merge(donors_dedup,merge, on='JHAS ID')

# #ALUMNI
alumni=pd.read_csv('/Users/loganlaberge/Work_2/ONEHopkins/Alums.csv',dtype={'JHAS ID':'string'})
alumni

alumni_agg = alumni.groupby('JHAS ID')['Degree: Degree'].agg(lambda x: ', '.join(x)).reset_index()


alumni_dedup=alumni.drop_duplicates(subset=['JHAS ID'])
alumni_withagg=pd.merge(alumni_dedup,alumni_agg,on='JHAS ID')
alumni_withagg['Degree: Degree_x'] = alumni_withagg['Degree: Degree_y']
alumni_withagg=alumni_withagg.drop('Degree: Degree_y', axis=1)
alumni_withagg=alumni_withagg.rename(columns={'Degree: Degree_x':'Degree: Degree'})
merged_alumni=pd.merge(alumni_withagg,merge, on='JHAS ID', how='left')

merged_alumni=merged_alumni.fillna({'Prior FYs': '0', 'This FY':'0','Most Recent Gift':'N/A', 'Most Recent Pledge':'N/A'})

#All Together

total_list=pd.concat([merged_alumni,merged_donors])
total_list

#OneHopkins
file_path = '/Users/loganlaberge/Work_2/ONEHopkins/OneHopkins25_Master.xlsx'

# Specify the sheets you want to load
sheets_to_load = ['Colette','Jaze','Julia','Kirsten','Zanieca','Katie','Logan','Talia']  # List of sheet names you want to load

# Read the specified sheets into a dictionary of dataframes
sheets_dict = pd.read_excel(file_path, sheet_name=sheets_to_load)

# Concatenate the selected sheets into a single dataframe
splitlist = pd.concat(sheets_dict.values(), ignore_index=True)

splitlist

#MoMENT OF TRUTH

splitlist_columns=['Divide Up','Salutation','First Name','Last Name', 'Email']
splitlist_info=splitlist[splitlist_columns]

One_Hopkins=pd.merge(total_list,splitlist_info, on=['Salutation','First Name','Last Name', 'Email'])




One_Hopkins.to_excel('One_Hopkins_Master2.xlsx')