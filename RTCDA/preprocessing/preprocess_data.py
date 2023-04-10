import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("data/raw_data/2017_2_clickstream.tsv", sep='\t', header=0)
    df = df[['prev_title', 'curr_title', 'n', 'type']]
    df = df.sort_values(by='n', ascending=False)[:1000]
    df.to_csv('data/preprocessed_data.csv', index=False)
