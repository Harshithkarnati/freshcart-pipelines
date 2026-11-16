
def transform(df):
    """
    Split the Iris dataset into 80% training and 20% testing data.
    """
    df = df.copy()
    df["split"] = "train"

    test_indices = df.sample(
        frac=0.2,
        random_state=42
    ).index

    df.loc[test_indices, "split"] = "test"

    return df


# Mage transformer block
try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    transformer = None
    test = None


if transformer is not None:

    @transformer
    def prepare_data(df, *args, **kwargs):
        return transform(df)

    @test
    def test_output(output, *args):
        assert output is not None
        assert len(output) == 150
        assert (output["split"] == "train").sum() == 120
        assert (output["split"] == "test").sum() == 30
