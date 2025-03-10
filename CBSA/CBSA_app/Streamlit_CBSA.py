import streamlit as st
import pandas as pd

CBSA=pd.read_csv('/Users/loganlaberge/Work_2/CBSA/ZIP_CBSA_Combined.csv', dtype={'ZIP':'string', 'CBSA':'string'})




def lookup_zips(location):
   zips_df=CBSA[CBSA['CBSA Title'] == location]
   zips_list=zips_df['ZIP'].tolist()
   if len(zips_list) > 213:
       first_list=zips_list[:213]
       everything_else=zips_list[213:]
       return [first_list, everything_else]
   else:
       return [zips_list]

def lookup_everything(location):
   df = CBSA[CBSA.Locale == location]
   zips_list = df['Zip'].tolist()
   if len(zips_list) > 222:
       first_list=zips_list[:222]
       everything_else=zips_list[222:]
       return [first_list, everything_else]
   else:
       return [zips_list]


lookup_zips('New York-Newark-Jersey City, NY-NJ')

def landing_page():
   st.title("CBSA Work Around")
   state_names = list(CBSA['State'].unique()).sort()
   if selected_options := st.multiselect("Select State(s):", state_names):
      holding_tank=[]
      for thing in selected_options:
         snip=CBSA[CBSA.State == thing]
         thing = list(snip['Locale'].unique()).sort()
         holding_tank.extend(iter(thing))
      if locale_options:= st.multiselect('Select Cities:', holding_tank):
         for town in locale_options:
            town_zip=lookup_everything(town)
            if len(town_zip) == 1:
               csv_list=""
               for count,entry in town_zip.enumerate():
                  if count in [0, len(town_zip) - 1]:
                     f'{csv_list}{entry}'
                  else:
                     f'{csv_list}{entry},'
               st.markdown(f'{town}')
               st.text_area(f'{csv_list}')
            else:
               csv_list_1=""
               csv_list_2=""
               for count,entry in town_zip[0].enumerate():
                  if count in [0, len(town_zip) - 1]:
                     csv_list+f'{entry}'
                  else:
                     csv_list+f'{entry},'
               for count,entry in town_zip[1].enumerate():
                  if count in [0, len(town_zip) - 1]:
                     csv_list+f'{entry}'
                  else:
                     csv_list+f'{entry},'
               st.markdown(f'{town}')
               st.markdown('First Filter')
               st.text_area(f'{csv_list_1}')
               st.markdown('Second Filter')
               st.text_area(f'{csv_list_1}')

   else:
      st.write("No state selected.")

if __name__ == "__main__":
    landing_page()

