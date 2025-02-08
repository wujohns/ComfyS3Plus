from .nodes.save_image_s3 import SaveImageS3
from .nodes.save_image_webp_s3 import SaveImageWebpS3
from .nodes.save_video_files_s3 import SaveVideoFilesS3
from .nodes.save_audio_s3 import SaveAudioS3
from .nodes.load_image_url import LoadImageByUrlOrPath
from .nodes.load_audio_url import LoadAudioByUrlOrPath

NODE_CLASS_MAPPINGS = {
    "SaveImageS3": SaveImageS3,
    "SaveImageWebpS3": SaveImageWebpS3,
    "SaveVideoFilesS3": SaveVideoFilesS3,
    "SaveAudioS3": SaveAudioS3,
    "LoadImageByUrlOrPath": LoadImageByUrlOrPath,
    "LoadAudioByUrlOrPath": LoadAudioByUrlOrPath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageS3": "Save Image to S3",
    "SaveImageWebpS3": "Save Image As Webp to S3",
    "SaveVideoFilesS3": "Save Video Files to S3",
    "SaveAudioS3": "Save Audio to S3",
    "LoadImageByUrlOrPath": "Load Image By Url Or Path",
    "LoadAudioByUrlOrPath": "Load Audio By Url Or Path"
}