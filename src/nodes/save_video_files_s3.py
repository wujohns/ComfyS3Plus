import os

from ..client_s3 import get_s3_instance
S3_INSTANCE = get_s3_instance()


class SaveVideoFilesS3:
    def __init__(self):
        self.s3_output_dir = os.getenv("S3_OUTPUT_DIR")
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "filename_prefix": ("STRING", {"default": "VideoFiles"}),
            "filenames": ("VHS_FILENAMES", )
            }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("s3_video_paths",)
    FUNCTION = "save_video_files"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "ComfyS3Plus"

    def save_video_files(self, filenames, filename_prefix="VideoFiles"):
        filename_prefix += self.prefix_append
        local_files = filenames[1]
        full_output_folder, filename, counter, subfolder, filename_prefix = S3_INSTANCE.get_save_path(filename_prefix)

        results = list()
        s3_video_paths = list()
        
        for path in local_files:
            ext = path.split(".")[-1]
            file = f"{filename}_{counter:05}_.{ext}"
            
            # Upload the local file to S3
            s3_path = os.path.join(full_output_folder, file)
            
            file_path = S3_INSTANCE.upload_file(path, s3_path)
              
            # Add the s3 path to the s3_image_paths list
            s3_video_paths.append(file_path)

            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

            # delete file
            if path and os.path.exists(path):
                os.remove(path)
    
        
        return { "ui": { "audios": results }, "result": (s3_video_paths, ) }
