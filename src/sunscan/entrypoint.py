import os
import json
import logging
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

from sunscan_process import predict_house_roofs
from definitions import BoundingBox

logger = logging.getLogger()
logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'INFO').upper()
)


# INPUTS_BASE_PATH = Path(os.environ.get('INPUTS_BASE_PATH', '/opt/ml/processing/inputs'))
OUTPUTS_BASE_PATH = Path(os.environ.get('OUTPUTS_BASE_PATH', '/opt/ml/processing/outputs'))
MODELS_BASE_PATH = Path(os.environ.get('MODELS_BASE_PATH', '/opt/ml/processing/models'))

DEFAULT_MODEL_NAME = 'sam_vit_h_4b8939.pth'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bounding-box', nargs=4, type=float, required=True)
    parser.add_argument('-m', '--model-name', type=str, default=DEFAULT_MODEL_NAME)

    payload = vars(parser.parse_args())

    logger.info(f'Payload: {payload}')
    return payload


def processing_routine(payload: dict, model_checkpoint: Path):
    logger.info('Initializing data inference.')

    with TemporaryDirectory() as tempdir:
        house_roofs_shp_path = predict_house_roofs(
            BoundingBox(*payload['bounding_box']),
            OUTPUTS_BASE_PATH,
            Path(tempdir),
            model_checkpoint
        )

    logger.info(house_roofs_shp_path)
    logger.info('Completed results export.')


if __name__ =='__main__':
    args = parse_args()

    model_checkpoint = MODELS_BASE_PATH / args['model_name']
    processing_routine(args, model_checkpoint)
