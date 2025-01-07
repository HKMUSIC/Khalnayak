from gtts import gTTS
def generate_tts(text):
    """
    Converts text to speech and saves it as 'shiv.mp3'.
    
    Args:
        text (str): The text to convert to speech.
    
    Returns:
        str: Path to the generated TTS file ('shiv.mp3').
    """
    path = "shiv.mp3"
    tts = gTTS(text)
    tts.save(path)
    return path