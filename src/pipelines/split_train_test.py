import argparse
import yaml
from ipywidgets import Text

from src.data.dataset import get_dataset
from src.transforms.trainsforms import transform_targets_to_numerics, split_dataset_in_train_test


def split_dataset(config_path: Text, base_config_path: Text):

    config = yaml.load(open(config_path), Loader=yaml.FullLoader)
    base_config = yaml.load(open(base_config_path), Loader=yaml.FullLoader)

    dataset = get_dataset(base_config['featurize']['dataset_csv'])
    target_column = base_config['featurize']['target_column']
    random_state = base_config['base']['random_state']

    test_size = config['test_size']
    train_csv_path = config['train_csv']
    test_csv_path = config['test_csv']

    dataset = transform_targets_to_numerics(dataset, target_column=target_column)

    train_dataset, test_dataset = split_dataset_in_train_test(dataset,
                                                              test_size=test_size,
                                                              random_state=random_state)

    train_dataset.to_csv(train_csv_path, index=False)
    test_dataset.to_csv(test_csv_path, index=False)



if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args_parser.add_argument('--base_config', dest='base_config', required=True)
    args = args_parser.parse_args()

    split_dataset(config_path=args.config, base_config_path=args.base_config)

