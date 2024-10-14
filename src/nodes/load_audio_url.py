# 从 url 中加载 audio
import torchaudio
import requests
from io import BytesIO

class LoadAudioByUrlOrPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url_or_path": ("STRING", {"multiline": True, "dynamicPrompts": False})
            }
        }

    RETURN_TYPES = ("AUDIO", )
    FUNCTION = "load"
    CATEGORY = "ComfyS3Plus"

    def load(self, url_or_path):
        print(url_or_path)
        if url_or_path.startswith('http'):
            response = requests.get(url_or_path)
            waveform, sample_rate = torchaudio.load(BytesIO(response.content))
            audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
            return (audio, )
        else:
            waveform, sample_rate = torchaudio.load(url_or_path)
            audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
            return (audio, )
