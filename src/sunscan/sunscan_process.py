from pathlib import Path

import leafmap
from samgeo.text_sam import LangSAM

from definitions import BoundingBox

MAP_ZOOM = 20
MAP_SOURCE = 'SATELLITE'
SAM_TEXT_PROMPT = 'houses'


def predict_house_roofs(
    bounding_box: BoundingBox,
    outputs_path: Path,
    tempdir_path: Path,
    model_checkpoint: Path = None,
) -> Path:

    map_tiles_path = outputs_path / 'map_tiles.tif'
    leafmap.tms_to_geotiff(
        map_tiles_path.as_posix(),
        bounding_box.as_list(),
        zoom=MAP_ZOOM,
        source=MAP_SOURCE
    )

    prediction_path = tempdir_path / f'{map_tiles_path.stem}_{SAM_TEXT_PROMPT}.tif'
    sam = LangSAM(checkpoint=model_checkpoint)

    sam.predict(
        map_tiles_path.as_posix(),
        SAM_TEXT_PROMPT,
        box_threshold=0.24,
        text_threshold=0.24,
        output=prediction_path.as_posix()
    )

    prediction_shp_path = prediction_path.with_suffix('.shp')
    sam.raster_to_vector(prediction_path, prediction_shp_path)

    return prediction_shp_path
