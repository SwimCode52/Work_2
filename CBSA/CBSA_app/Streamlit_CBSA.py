import streamlit as st
import pandas as pd

CBSA=pd.read_csv('ZIP_CBSA_Combined.csv', dtype={'ZIP':'string', 'CBSA':'string'})




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
   df_nodup=df.drop_duplicates(subset='ZIP')
   zips_list = df_nodup['ZIP'].tolist()
   if len(zips_list) > 222:
       first_list=zips_list[:222]
       everything_else=zips_list[222:]
       return [first_list, everything_else]
   else:
       return [zips_list]


lookup_zips('New York-Newark-Jersey City, NY-NJ')

def landing_page():
   st.title("CBSA Work Around")

   state_names = list(CBSA['State'].unique())
   if selected_options := st.multiselect("Select State(s):", sorted(state_names)):
      holding_tank = []

      for thing in selected_options:
          snip = CBSA[CBSA.State == thing]
          thing = list(snip['Locale'].unique())
          holding_tank.extend(thing)

      if locale_options := st.multiselect('Select Cities:', sorted(holding_tank)):
         for town in locale_options:
            town_zip = lookup_everything(town)

            if len(town_zip) == 1:
               csv_list = "".join(
                    f"{entry}, " if count < len(town_zip[0]) - 1 else f"{entry}"
                    for count, entry in enumerate(town_zip[0])
                )
               st.markdown(f'**{town}**')
               st.text_area("ZIP Codes:", csv_list)  # Corrected argument

            else:
               csv_list_1 = ""
               csv_list_2 = ""

               for count, entry in enumerate(town_zip[0]):  # First filter
                  if count == 0:
                     csv_list_1 += f'{entry}, '
                  elif count == len(town_zip[0]) - 1:
                     csv_list_1 += f'{entry}'
                  else:
                     csv_list_1 += f'{entry}, '

               for count, entry in enumerate(town_zip[1]):  # Second filter
                  if count == 0:
                     csv_list_2 += f'{entry}, '
                  elif count == len(town_zip[0]) - 1:
                     csv_list_2 += f'{entry}'
                  else:
                     csv_list_2 += f'{entry}, '

               st.markdown(f'**{town}**')
               st.markdown('**First Filter**')
               st.text_area("ZIP Codes (First 222):", csv_list_1)
               st.markdown('**Second Filter**')
               st.text_area("Remaining ZIP Codes:", csv_list_2)

   else:
      st.write("No state selected.")

if __name__ == "__main__":
    landing_page()

