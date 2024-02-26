import os
import logging
import argparse
import datetime
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import geopandas as gpd

from definitions import BoundingBox
from sunscan_process import predict_house_roofs
from solar_energy import calculate_solar_energy

logger = logging.getLogger()
logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'INFO').upper()
)

MODELS_BASE_PATH = Path(os.environ.get('MODELS_BASE_PATH', '/opt/ml/processing/models'))
OUTPUTS_BASE_PATH = Path(os.environ.get('OUTPUTS_BASE_PATH', '/opt/ml/processing/outputs'))

DEFAULT_MODEL_NAME = 'sam_vit_h_4b8939.pth'


def parse_args() -> dict:
    parser = argparse.ArgumentParser(
        description='Calculate sun power collected by solar panels on roofs.'
    )
    parser.add_argument(
        '-b', '--bounding-box',
        help='The bounding box [minx, miny, maxx, maxy] coordinates in EPSG:4326',
        nargs=4,
        type=float,
        required=True
    )
    parser.add_argument(
        '--panel-size',
        help='Solar panel size in square meters',
        type=float,
        required=True
    )
    parser.add_argument(
        '--available-area',
        help='Roof availability to install panels in percentage',
        type=float,
        required=True
    )
    parser.add_argument(
        '--panel-power',
        help='Solar panel power in watts',
        type=int,
        required=True
    )
    parser.add_argument(
        '--dimension-factor',
        type=float,
        default=0.8
    )

    payload = vars(parser.parse_args())

    logger.info(f'Payload: {payload}')
    return payload


def zip_shp_result(gdf: gpd.GeoDataFrame, zip_path: Path):
    with TemporaryDirectory() as tempdir:
        temp_path = Path(tempdir) / 'solar_energy'
        gdf.to_file(temp_path)

        with ZipFile(zip_path.as_posix(), mode='w') as archive:
            for file_path in temp_path.iterdir(): 
                archive.write(file_path.as_posix(), file_path.name)


def processing_routine(payload: dict, model_checkpoint: Path):
    logger.info('Initializing data inference.')

    with TemporaryDirectory() as tempdir:
        house_roofs_shp_path = predict_house_roofs(
            BoundingBox(*payload['bounding_box']),
            OUTPUTS_BASE_PATH,
            Path(tempdir),
            model_checkpoint
        )

        # TODO: Check these parameters.
        start = datetime.datetime(2024, 1, 1)
        end = datetime.datetime(2024, 12, 31)

        solar_energy = calculate_solar_energy(
            house_roofs_shp_path,
            start,
            end,
            payload['panel_size'],
            payload['available_area'],
            payload['panel_power'] / 1000,
            payload['dimension_factor']
        )

        # TODO: WARNING:fiona._env:Normalized/laundered field name:
        # 'Energia_acum' to 'Energia_ac'
        # 'Energia_diaria' to 'Energia_di'
        # 'Energia_anual' to 'Energia_an'
        zip_shp_result(solar_energy, OUTPUTS_BASE_PATH / 'solar_energy_shp.zip')
        solar_energy.to_excel(OUTPUTS_BASE_PATH / 'solar_energy.xlsx')

    logger.info('Completed results export.')


if __name__ =='__main__':
    args = parse_args()

    model_checkpoint = MODELS_BASE_PATH / DEFAULT_MODEL_NAME
    processing_routine(args, model_checkpoint)
