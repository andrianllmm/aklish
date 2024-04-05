import os
import pandas as pd


script_dir = os.path.dirname(os.path.realpath(__file__))


df = pd.read_excel(f"{script_dir}/akl_dictionary.xlsx", sheet_name="root_words")
df.to_csv(f"{script_dir}/akl_dictionary.csv", index=False)