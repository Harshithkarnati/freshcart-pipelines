
@transformer
def validate_iris(df, *args, **kwargs):
    # Check for missing values
    assert df.isnull().sum().sum() == 0, "Dataset contains missing values"

    # Check dataset size
    assert len(df) == 150, "Expected exactly 150 rows"

    # Check number of target classes
    assert df["target"].nunique() == 3, "Expected exactly 3 classes"

    print("Iris dataset validation successful!")
    return df


@test
def test_output(output, *args):
    assert output is not None
    assert len(output) == 150
    assert output.isnull().sum().sum() == 0
    assert output["target"].nunique() == 3
