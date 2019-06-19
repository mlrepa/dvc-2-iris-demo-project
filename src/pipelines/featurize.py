import argparse
from typing import Text

import yaml

from src.data.dataset import get_dataset
from src.features.features import extract_features


def featurize(config_path: Text):

    config = yaml.load(open(config_path), Loader=yaml.FullLoader)

    dataset = get_dataset(config['dataset_csv'])
    featured_dataset = extract_features(dataset)

    filpath = config['featured_dataset_csv']
    featured_dataset.to_csv(filpath, index=False)


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    featurize(config_path=args.config)