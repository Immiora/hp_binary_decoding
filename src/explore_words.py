'''

'''


import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

word_file = '/Fridge/users/julia/project_hp_reading/data/4pascal/sub-002/sub-002_ses-iemu_acq-ECOG_run-02_audio.csv'
all_words = pd.read_csv(word_file)

##
all_words['text'].value_counts()[:100].plot(kind='bar')
# meneer 31 and mevrouw 18
# perkamentus and anderling