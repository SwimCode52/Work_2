import streamlit as st
import pandas as pd

Correct_CBSA=pd.read_csv('CBSA/CBSA_app/ZIP_CBSA_Combined.csv', dtype={'ZIP':'string', 'CBSA':'string'})
MC_CBSA=pd.read_csv('CBSA/CBSA_app/MarketingCloud_Zip.csv', dtype={'ZIP':'string', 'CBSA':'string'})

#ForDebugging
# Correct_CBSA=pd.read_csv('/Users/loganlaberge/Work_2/CBSA/ZIP_CBSA_Combined.csv', dtype={'ZIP':'string', 'CBSA':'string'})
# MC_CBSA=pd.read_csv('/Users/loganlaberge/Work_2/CBSA/CBSA_app/MarketingCloud_Zip.csv', dtype={'ZIP':'string', 'CBSA':'string'})


def lookup_zips(location):
   zips_df=CBSA[CBSA['CBSA Title'] == location]
   zips_list=zips_df['ZIP'].tolist()
   if len(zips_list) > 213:
       first_list=zips_list[:213]
       everything_else=zips_list[213:]
       return [first_list, everything_else]
   else:
       return [zips_list]

def lookup_everything(location, CBSA):
   df = CBSA[CBSA.Locale == location]
   df_nodup=df.drop_duplicates(subset='ZIP')
   zips_list = df_nodup['ZIP'].tolist()
   if len(zips_list) > 222:
       first_list=zips_list[:222]
       everything_else=zips_list[222:]
       if len(everything_else) > 222:
          second_list= everything_else[:222]
          last_list=everything_else[222:]
          return [first_list, second_list,last_list]
       else:
         return [first_list, everything_else]
   else:
       return [zips_list]


# lookup_zips('New York-Newark-Jersey City, NY-NJ')

def landing_page():
   st.title("CBSA Work Around")
   option = st.selectbox(
    'Select your Dataset:',
    ('','HUD CBSA List', 'MarketingCloud List')
)
   st.write('You selected:', option)
   if option == 'HUD CBSA List':
       CBSA=Correct_CBSA
       st.markdown(""" This option is the most up to date CBSA Data but :red[**does not match Marketing Cloud and should not be used in financial reporting**]""")
   elif option == 'MarketingCloud List':
       CBSA=MC_CBSA
       st.markdown('This selection matches the current mapping for Marketing Cloud.')
   else:
      st.markdown(' Please select option')

   if option in ['HUD CBSA List', 'MarketingCloud List']:
      state_names = list(CBSA['State'].unique())
      if selected_options := st.multiselect("Select State(s):", sorted(state_names)):
         holding_tank = []

         for thing in selected_options:
            snip = CBSA[CBSA.State == thing]
            thing = list(snip['Locale'].unique())
            holding_tank.extend(thing)

         if locale_options := st.multiselect('Select Cities:', sorted(holding_tank)):
            for town in locale_options:
               town_zip = lookup_everything(town, CBSA)

               if len(town_zip) == 1:
                  csv_list = "".join(
                     f"{entry}, " if count < len(town_zip[0]) - 1 else f"{entry}"
                     for count, entry in enumerate(town_zip[0])
                  )
                  st.markdown(f'**{town}**')
                  st.text_area("ZIP Codes:", csv_list)  # Corrected argument

               elif len(town_zip)==2:
                  csv_list_1 = ""
                  csv_list_2 = ""

                  for count, entry in enumerate(town_zip[0]):  # First filter
                     if count == 0:
                        csv_list_1 += f'{entry},'
                     elif count == len(town_zip[0]) - 1:
                        csv_list_1 += f'{entry}'
                     else:
                        csv_list_1 += f'{entry},'

                  for count, entry in enumerate(town_zip[1]):  # Second filter
                     if count == 0:
                        csv_list_2 += f'{entry},'
                     elif count == len(town_zip[1]) - 1:
                        csv_list_2 += f'{entry}'
                     else:
                        csv_list_2 += f'{entry},'

                  st.markdown(f'**{town}**')
                  st.markdown('**First Filter**')
                  st.text_area("ZIP Codes (First 222):", csv_list_1)

                  st.divider()

                  st.markdown('**Second Filter**')
                  st.text_area("Remaining ZIP Codes:", csv_list_2)
               else:
                  csv_list_1 = ""
                  csv_list_2 = ""
                  csv_list_3 = ""

                  for count, entry in enumerate(town_zip[0]):  # First filter
                     if count == 0:
                        csv_list_1 += f'{entry},'
                     elif count == len(town_zip[0]) - 1:
                        csv_list_1 += f'{entry}'
                     else:
                        csv_list_1 += f'{entry},'

                  for count, entry in enumerate(town_zip[1]):  # Second filter
                     if count == 0:
                        csv_list_2 += f'{entry},'
                     elif count == len(town_zip[1]) - 1:
                        csv_list_2 += f'{entry}'
                     else:
                        csv_list_2 += f'{entry},'
                  for count, entry in enumerate(town_zip[2]):  # Second filter
                     if count == 0:
                        csv_list_3 += f'{entry},'
                     elif count == len(town_zip[2]) - 1:
                        csv_list_3 += f'{entry}'
                     else:
                        csv_list_3 += f'{entry},'
                  

                  st.markdown(f'**{town}**')
                  st.markdown('**First Filter**')
                  st.text_area("ZIP Codes (First 222):", csv_list_1)

                  st.divider()

                  st.markdown('**Second Filter**')
                  st.text_area("Second Filter:", csv_list_2)

                  st.divider()

                  st.markdown('**Third Filter**')
                  st.text_area("Remaining ZIP Codes:", csv_list_3)

      else:
         st.write("No state selected.")

if __name__ == "__main__":
    landing_page()

