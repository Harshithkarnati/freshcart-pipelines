
from sklearn.datasets import load_iris
import pandas as pd


@data_loader
def load_iris_data(*args, **kwargs):
    iris = load_iris(as_frame=True)
    return iris.frame


@test
def test_output(output, *args):
    assert output is not None
    assert len(output) == 150
    assert output.shape[1] == 5
    assert "target" in output.columns
    assert output["target"].nunique() == 3
