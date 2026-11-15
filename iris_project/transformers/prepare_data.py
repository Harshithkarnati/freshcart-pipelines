
def transform(df):
    """
    Add a split column to the Iris dataset.
    80% of rows are assigned to train and 20% to test.
    """
    df = df.copy()

    df["split"] = "train"
    df.loc[df.sample(frac=0.3, random_state=42).index, "split"] = "test"

    return df
