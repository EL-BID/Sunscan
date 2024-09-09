# https://docs.aws.amazon.com/deep-learning-containers/latest/devguide/deep-learning-containers-images.html
# https://github.com/aws/deep-learning-containers/blob/master/available_images.md

FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:2.1.0-gpu-py310-cu121-ubuntu20.04-sagemaker

RUN apt update \
    && apt install --no-install-recommends -y binutils libproj-dev gdal-bin libgdal-dev \
    && apt clean

RUN python3 -m pip install --upgrade pip --no-cache-dir \
    && pip3 install --upgrade --no-cache-dir astral==3.2 groundingdino-py==0.4.0 leafmap==0.31.3 openpyxl==3.1.2 segment-geospatial==0.10.2

RUN pip3 install setuptools==57.5.0 \
    && pip3 install gdal==$(gdal-config --version)
