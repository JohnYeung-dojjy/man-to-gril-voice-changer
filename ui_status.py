from dataclasses import dataclass

@dataclass
class VoiceChangerStatus:
    mic_on: bool = False
    voice_changing: bool = False
    denoising: bool = False