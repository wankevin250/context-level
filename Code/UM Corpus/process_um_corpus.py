import pandas as pd
import re as re

path = 'Bi-News.txt'

english_output_path = 'UM_english_news_data.xlsx'

chinese_output_path = 'UM_chinese_news_data.xlsx'

with open(path, 'r') as f:
    all_lines = f.readlines()

    # Remove newline characters from each line
    all_lines = [line.strip() for line in all_lines]

    # Separate lines into two lists: even-indexed and odd-indexed
    column1_data = all_lines[::2]  # Every other line starting from the first (index 0)
    column2_data = all_lines[1::2] # Every other line starting from the second (index 1)

english_df = pd.DataFrame({'utterance': column1_data})
english_df.reset_index(inplace=True)
english_df.rename(columns={'index': 'utterance_id'}, inplace=True)
english_df['utterance_id'] = "u" + english_df['utterance_id'].astype("string")

chinese_df = pd.DataFrame({'utterance': column2_data})
chinese_df.reset_index(inplace=True)
chinese_df.rename(columns={'index': 'utterance_id'}, inplace=True)
chinese_df['utterance_id'] = "u" + chinese_df['utterance_id'].astype("string")

# print(english_df)
# print(chinese_df)
ILLEGAL_CHARACTERS_RE = re.compile(r'[\x00-\x1F\x7F]')

# Apply the replacement to all string columns
for col in english_df.select_dtypes(include=['object']).columns:
    english_df[col] = english_df[col].str.replace(ILLEGAL_CHARACTERS_RE, '', regex=True)

for col in chinese_df.select_dtypes(include=['object']).columns:
    chinese_df[col] = chinese_df[col].str.replace(ILLEGAL_CHARACTERS_RE, '', regex=True)

english_df.to_excel(english_output_path)
chinese_df.to_excel(chinese_output_path)