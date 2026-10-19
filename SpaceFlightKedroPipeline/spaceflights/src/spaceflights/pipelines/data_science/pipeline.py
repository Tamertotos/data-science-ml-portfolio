"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.7.0
"""

from kedro.pipeline import Node, Pipeline  # noqa
from .nodes import evaluate_model, train_model, split_data

def create_pipeline(**kwargs) -> Pipeline:
    pipeline_instance = Pipeline(
        [
            Node(
                func= split_data,
                inputs= ["model_input_table","params:model_options"],
                outputs= ["X_train", "X_test", "y_train", "y_test"],
                name= "split_data_node"
            ),
            Node(
                func= train_model,
                inputs= ["X_train","y_train"],
                outputs= "model",
                name= "train_model_node"
            ),
            Node(
                func= evaluate_model,
                inputs= ["model","X_test", "y_test"],
                outputs= None,
                name= "evaluate_model_node"
            ),
        ]
    )

    ds_pipeline_1 = Pipeline(
        nodes=pipeline_instance,
        inputs="model_input_table",
        namespace="active_modelling_pipeline"
    )
    ds_pipeline_2 = Pipeline(
        nodes=pipeline_instance,
        inputs="model_input_table",
        namespace="candidate_modelling_pipeline"
    )

    return ds_pipeline_1 + ds_pipeline_2