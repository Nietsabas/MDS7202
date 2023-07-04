"""
This is a boilerplate pipeline 'train_model'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node, pipeline
from nodes import split_data, train_model, evaluate_model
from kedro.io import DataCatalog
from kedro.runner import SequentialRunner


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                split_data,
                inputs="data",
                outputs=[
                    "X_train",
                    "X_valid",
                    "X_test",
                    "y_train",
                    "y_valid",
                    "y_test",
                ],
                name="split_data_node",
            ),
            node(
                train_model,
                inputs=[
                    "X_train",
                    "X_valid",
                    "y_train",
                    "y_valid",
                ],
                outputs="best_model",
                name="train_model_node",
            ),
            node(
                evaluate_model,
                inputs=["best_model", "X_test", "y_test"],
                outputs=None,
                name="evaluate_model_node",
            ),
        ]
    )


def run_pipelines(pipeline, catalog):
    runner = SequentialRunner()
    runner.run(pipeline, catalog)


if __name__ == "__main__":
    parameters = dict(
        split_params=dict(
            target="price",
            train_ratio=0.8,
            valid_ratio=0.1,
            random_state=67
        )
    )
    catalog = DataCatalog.from_config("conf/base/catalog.yml")
    pipeline = create_pipeline(**parameters)
    run_pipelines(pipeline, catalog)

