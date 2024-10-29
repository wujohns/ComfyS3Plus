# 保存 audio 到 s3
import os
import io
import tempfile
import torchaudio
import time

from ..client_s3 import get_s3_instance_plus

class SaveAudioS3:
    def __init__(self):
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # 功能参数相关
                "audio": ("AUDIO", ),
                "filename_prefix": ("STRING", {"default": "Audio"}),

                # s3 存储相关
                "version": ("STRING", ),
                "region": ("STRING", ),
                "access_key": ("STRING", ),
                "secret_key": ("STRING", ),
                "bucket_name": ("STRING", ),
                "endpoint_url": ("STRING", ),
                "input_dir": ("STRING", ),
                "output_dir": ("STRING", )
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("s3_audio_paths",)
    FUNCTION = "save_audio"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "ComfyS3Plus"

    def save_audio(
        # base param
        self, 
        audio,
        filename_prefix,

        # s3 存储相关
        version, region, access_key, secret_key, bucket_name,
        endpoint_url, input_dir, output_dir,

        # hidden param
        prompt=None,
        extra_pnginfo=None
    ):
        S3_INSTANCE = get_s3_instance_plus(
            version=version,
            region=region,
            access_key=access_key,
            secret_key=secret_key,
            bucket_name=bucket_name,
            endpoint_url=endpoint_url,
            input_dir=input_dir,
            output_dir=output_dir
        )
        filename_prefix += f"{ int(round(time.time() * 1000)) }"
        full_output_folder, filename, counter, subfolder, filename_prefix = S3_INSTANCE.get_save_path(filename_prefix)
        results = list()
        s3_audio_paths = list()

        for (batch_number, waveform) in enumerate(audio["waveform"].cpu()):
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.mp3"

            temp_file = None
            try:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    temp_file_path = temp_file.name

                    # Save the audio to the temporary file
                    buff = io.BytesIO()
                    torchaudio.save(buff, waveform, audio["sample_rate"], format="mp3")
                    with open(temp_file_path, 'wb') as f:
                        f.write(buff.getbuffer())

                    # Upload the temporary file to S3
                    s3_path = os.path.join(full_output_folder, file)
                    file_path = S3_INSTANCE.upload_file(temp_file_path, s3_path)

                    # Add the s3 path to the s3_audio_paths list
                    s3_audio_paths.append(file_path)

                    # Add the result to the results list
                    results.append({
                        "filename": file,
                        "subfolder": subfolder,
                        "type": self.type
                    })
                    counter += 1
            finally:
                # Delete the temporary file
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        return { "ui": { "audios": results }, "result": (s3_audio_paths, ) }
