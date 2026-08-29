import parameter_mappers as mappers

MODEL_NAME = 'sam_vit_h_4b8939.pth'


class InferenceBuilder(object):
    def __init__(self, task_key: str, base_code_s3uri: str, attachments_bucket_name: str):
        self.task_key = task_key
        self.base_code_s3uri = base_code_s3uri
        self.attachments_bucket_name = attachments_bucket_name

    def build_inference_parameters(self, payload):
        return {
            'JobName': mappers.get_unique_job_name(self.task_key, 'roof-energy'),
            'ContainerArguments': payload['container_args'],
            'InputConfig': [
                mappers.get_processing_input(
                    'code',
                    self.base_code_s3uri + '/code',
                    '/opt/ml/processing/code'
                ),
                mappers.get_processing_input(
                    'models',
                    self.base_code_s3uri + f'/{MODEL_NAME}',
                    '/opt/ml/processing/models'
                )
            ],
            'OutputConfig': [
                mappers.get_processing_output('outputs',
                    '/opt/ml/processing/outputs', payload['inference_outputs_uri'])
            ]
        }

    def run(self, inputs: dict, user_sub: str):
        inference_container_args = [
            '--bounding-box', *[str(coord) for coord in inputs['BoundingBox']],
            '--panel-size', str(inputs['PanelSize']),
            '--available-area', str(inputs['AvailableArea']),
            '--panel-power', str(inputs['PanelPower'])
        ]

        payload = {
            'task_key': self.task_key,
            'container_args': inference_container_args,
            'inference_outputs_uri': f's3://{self.attachments_bucket_name}/sunscan/user:{user_sub}/roof_energy/{self.task_key}/outputs/'
        }

        return self.build_inference_parameters(payload)
