import datetime as dt

def get_unique_job_name(uuid_key: str, *references: list):
    """ Returns a unique job name based on a given uuid_key
        and the current timestamp """

    return '-'.join([
        *uuid_key.split('-')[:2],
        dt.datetime.utcnow().strftime('%Y%m%d-%H%M%S'),
        *references
    ])[:63]

def get_processing_input(name: str, inputs_s3_uri: str, output_local_path: str):
    return {
        'InputName': name,
        'S3Input': {
            'S3DataType': 'S3Prefix',
            'S3Uri': inputs_s3_uri,
            'LocalPath': output_local_path,
            'S3DataDistributionType': 'FullyReplicated',
            'S3InputMode': 'File'
        }
    }

def get_processing_output(name: str, input_local_path: str, outputs_s3_uri: str):
    return {
        'OutputName': name,
        'S3Output': {
            'LocalPath': input_local_path,
            'S3Uri': outputs_s3_uri,
            'S3UploadMode': 'EndOfJob'
        }
    }
