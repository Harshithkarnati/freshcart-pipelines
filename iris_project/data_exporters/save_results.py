
import os


@data_exporter
def save_results(df, *args, **kwargs):
    output_path = "/content/iris_predictions.csv"

    df.to_csv(output_path, index=False)

    print(f"Predictions saved to: {output_path}")

    return df


@test
def test_output(output, *args):
    assert output is not None
    assert len(output) == 30
    assert "actual" in output.columns
    assert "predicted" in output.columns
