import os
import logging

from inference_builder import InferenceBuilder

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.CRITICAL)

BASE_CODE_S3URI = os.getenv('BASE_CODE_S3URI')
ATTACHMENTS_BUCKET_NAME = os.getenv('ATTACHMENTS_BUCKET_NAME')


def lambda_handler(event: dict, context):
    builder = InferenceBuilder(
        event['TaskKey'],
        BASE_CODE_S3URI,
        ATTACHMENTS_BUCKET_NAME
    )

    payload = builder.run(
        event['Inputs'],
        user_sub=event['UserSub']
    )

    return payload
