from utils import get_client
import tempfile
import os

async def process_media(audio_bytes=None, image_bytes=None, extra_prompt=None):
    client = get_client()
    inputs = []

    if audio_bytes:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        audio_file = client.files.upload(file=tmp_path)
        os.unlink(tmp_path)  # cleanup temp file
        inputs.append(audio_file)

    if image_bytes:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(image_bytes)
            tmp_path = tmp_file.name
        img_file = client.files.upload(file=tmp_path)
        os.unlink(tmp_path)  # cleanup temp file
        inputs.append(img_file)

    if extra_prompt:
        inputs.insert(0, extra_prompt)

    result = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=inputs
    )
    return result.text