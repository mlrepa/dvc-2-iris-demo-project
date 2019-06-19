
import argparse
from typing import Text
import yaml


def prepare_configs(config_path: Text):
    """
    Split common config into configs for steps
    """

    config = yaml.load(open(config_path), Loader=yaml.FullLoader)
    experiments_folder = config['base']['experiments']['experiments_folder']

    for config_name, config_params in config.items():

        filepath = f'{experiments_folder}/{config_name}_config.yml'
        with open(filepath, 'w') as config_file:
            yaml.dump(
                data=config_params,
                stream=config_file,
                default_flow_style=False
            )
            print(f'Save config: {filepath}')

if __name__ == '__main__':

    # parse arguments
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    prepare_configs(config_path=args.config)
