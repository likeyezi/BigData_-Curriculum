import pandas as pd
df = pd.read_csv('input_to_clean.csv')
user_counts = df['顾客编号'].value_counts()
valid_users = user_counts[user_counts >= 20].index.tolist()
filtered_df = df[df['顾客编号'].isin(valid_users)]
filtered_df.to_csv('filtered_file.csv', index=False)

