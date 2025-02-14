# transcribr
Effortless Audio &amp; Video Transcription and Subtitle Generation

## Description:
transcribr is a simple Python package designed to automatically transcribe audio and video files into accurate text or subtitle formats (.srt). 
It supports multiple languages, offering fast and reliable speech recognition for creating subtitles or generating transcriptions for podcasts, lectures, interviews, and more. 
Built on state-of-the-art speech recognition models (OpenAI whisper), transcribr simplifies the process of turning spoken words into structured, searchable text.

## Key Features:
* Supports video (.mp4, .mov, etc.) and audio (.mp3, .wav, etc.) inputs
* Generates subtitle files (.srt) with precise timestamps
* Multilingual transcription capabilities
* Easy integration into Python workflows

## Use Cases:
* Automatic subtitle generation for videos
* Transcription of podcasts and interviews
* Creating searchable transcripts for lectures and meetings

## Get Started:
Install the package and generate your first transcription in minutes with just a few lines of code!

### Installation

```bash
pip install transcribr
```

### Example Usage

```python
from transcribr import Transcribr

video_file = "example.mp3"  # Replace with your video file path

# transcribe content
transcribr = Transcribr(model="base")
transcribr.transcribe(video_file)

# save transcription and subtitles
transcribr.save_transcription(output_file="output.txt")
transcribr.save_subtitles(output_file="output.srt")
