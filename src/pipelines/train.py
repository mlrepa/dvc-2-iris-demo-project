import argparse
from typing import Text

import joblib
import os
import yaml

from src.data.dataset import get_dataset
from src.train.train import train


def train_model(config_path: Text, base_config_path: Text):

    config = yaml.load(open(config_path), Loader=yaml.FullLoader)
    base_config = yaml.load(open(base_config_path), Loader=yaml.FullLoader)

    estimator_name = config['estimator_name']
    param_grid = config['estimators'][estimator_name]['param_grid']
    cv = config['cv']

    target_column = base_config['featurize']['target_column']
    train_df = get_dataset(base_config['split_train_test']['train_csv'])

    model = train(
        df=train_df,
        target_column=target_column,
        estimator_name=estimator_name,
        param_grid=param_grid,
        cv=cv
    )

    print(model.best_score_)

    model_name = base_config['base']['model']['model_name']
    models_folder = base_config['base']['model']['models_folder']

    joblib.dump(
        model,
        os.path.join(models_folder, model_name)
    )


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args_parser.add_argument('--base_config', dest='base_config', required=True)
    args = args_parser.parse_args()

    train_model(config_path=args.config, base_config_path=args.base_config)

