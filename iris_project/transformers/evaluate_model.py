
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report


@transformer
def evaluate_model(df, *args, **kwargs):
    actual = df["actual"]
    predicted = df["predicted"]

    # Generate confusion matrix
    cm = confusion_matrix(actual, predicted, labels=[0, 1, 2])

    cm_df = pd.DataFrame(
        cm,
        index=["Actual 0", "Actual 1", "Actual 2"],
        columns=["Predicted 0", "Predicted 1", "Predicted 2"]
    )

    # Generate classification metrics
    report = classification_report(
        actual,
        predicted,
        labels=[0, 1, 2],
        output_dict=True,
        zero_division=0
    )

    metrics_df = pd.DataFrame(report).T
    metrics_df = metrics_df.loc[
        ["0", "1", "2", "macro avg", "weighted avg"],
        ["precision", "recall", "f1-score", "support"]
    ]

    print("CONFUSION MATRIX")
    print(cm_df)

    print("\nCLASSIFICATION METRICS")
    print(metrics_df)

    return {
        "confusion_matrix": cm_df,
        "metrics": metrics_df
    }


@test
def test_output(output, *args):
    assert output is not None
    assert output["confusion_matrix"].shape == (3, 3)
    assert len(output["metrics"]) == 5
    assert output["confusion_matrix"].values.sum() == 30
