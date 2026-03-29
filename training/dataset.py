import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    return df

def preprocess(df):
    removed_data = []

    null_df = df[df["text"].isnull() | df["label"].isnull()].copy()
    null_df["reason"] = "null"
    removed_data.append(null_df)
    df = df.dropna(subset=["text", "label"])

    dup_df = df[df.duplicated(subset=["text"])].copy()
    dup_df["reason"] = "duplicate"
    removed_data.append(dup_df)
    df = df.drop_duplicates(subset=["text"])

    short_df = df[df["text"].str.len() <= 10].copy()
    short_df["reason"] = "too_short"
    removed_data.append(short_df)
    df = df[df["text"].str.len() > 10]

    invalid_label_df = df[~df["label"].isin([0, 1])].copy()
    invalid_label_df["reason"] = "invalid_label"
    removed_data.append(invalid_label_df)
    df = df[df["label"].isin([0, 1])]

    removed_data = [d for d in removed_data if len(d) > 0]

    if removed_data:
        removed_df = pd.concat(removed_data)
        removed_df.to_csv("data/processed/removed_data.csv", index=False)

    return df

def split_data(df):
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["label"],
        test_size=0.1,
        random_state=42,
        stratify=df["label"]
    )
    return X_train, X_test, y_train, y_test

def save_data(X_train, X_test, y_train, y_test):
    train_df = pd.DataFrame({"text": X_train, "label": y_train})
    test_df  = pd.DataFrame({"text": X_test,  "label": y_test})

    train_df.to_csv("data/processed/train.csv", index=False)
    test_df.to_csv("data/processed/test.csv", index=False)

if __name__ == "__main__":
    df = load_data("data/raw/AI_human_200k.csv")
    df = preprocess(df)
    X_train, X_test, y_train, y_test = split_data(df)
    save_data(X_train, X_test, y_train, y_test)