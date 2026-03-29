import pandas as pd
import matplotlib.pyplot as plt

def load_data(path):
    return pd.read_csv(path)

def basic_info(df):
    print(df.info())
    print(df.head())
    print(df.isnull().sum())

def label_distribution(df):
    df["Label"].value_counts().plot(kind="bar")
    plt.title("Label Distribution")
    plt.show()

def text_length_analysis(df):
    df["text_length"] = df["Text"].astype(str).apply(len)
    print(df["text_length"].describe())

    plt.hist(df["text_length"], bins=50)
    plt.title("Text Length")
    plt.show()

def sample_data(df):
    print(df[df["Label"] == 0]["Text"].head(2))
    print(df[df["Label"] == 1]["Text"].head(2))

def check_duplicates(df):
    print(df.duplicated(subset=["Text"]).sum())

if __name__ == "__main__":
    df = load_data("data/raw/AI_human_200k.csv")
    basic_info(df)
    label_distribution(df)
    text_length_analysis(df)
    sample_data(df)
    check_duplicates(df)