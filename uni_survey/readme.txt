Project performs some simple plotting/ statistical analysis of unicycle survey data

agelearn_2021_anonymised_20211025.xls: original received data file
agelearn_2021_anonymised_202110258.xls: sorted, some light cleaning of responses, switched language for Korean responses 

cleaning1_totrans.py: script that begins cleaning and coding data, employing the Google Translate API from deep_translator. Translating takes some computing time, so this script pickles the partially cleaned dataframe. pickled file is rawdf.pkl

The detailed questions (in English) from the header of the as-received Excel file are saved as verboseqs.csv

cleanin2.py: script that continues cleaning and coding data, and removes extraneous fields. I gave up automated cleaning some fields, so the tofix.csv output field values to be cleaned. Corrections were manually added to the tofix_manual.csv file, then reloaded to a dictionary to perform the corrections.

cleaned_data.csv is the database in a mostly cleaned state.

eda.py performs some plotting and statistical analyses