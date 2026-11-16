
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


@transformer
def train_model(df, *args, **kwargs):
    max_depth = int(kwargs.get("max_depth", 3))

    train_df = df[df["split"] == "train"]
    test_df = df[df["split"] == "test"]

    feature_cols = [
        col for col in df.columns
        if col not in ["target", "split"]
    ]

    X_train = train_df[feature_cols]
    y_train = train_df["target"]

    X_test = test_df[feature_cols]
    y_test = test_df["target"]

    model = DecisionTreeClassifier(
        max_depth=max_depth,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    results = pd.DataFrame({
        "actual": y_test.to_numpy(),
        "predicted": predictions,
        "test_accuracy": accuracy,
        "max_depth": max_depth
    })

    return results


@test
def test_output(output, *args):
    assert output is not None
    assert len(output) == 30

    accuracy = float(output["test_accuracy"].iloc[0])

    assert accuracy > 0.80, (
        f"Test accuracy too low: {accuracy:.2%}"
    )
