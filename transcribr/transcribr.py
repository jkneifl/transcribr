import whisper
import os
import ffmpeg
from datetime import timedelta
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class Transcribr:

    def __init__(self, model="base"):

        assert model in [
            "tiny",
            "base",
            "small",
            "medium",
            "large",
            "turbo",
        ], "Invalid model size. Choose from 'tiny', 'base', 'small', 'medium', 'large', or 'turbo'."

        logging.info(f"Loading Whisper model: {model}")
        self.model = whisper.load_model(model)
        self.transcription = None
        self.file_path = None

    def transcribe(self, file_path):
        """Transcribes audio using Whisper."""

        assert os.path.exists(file_path), f"File '{file_path}' not found."

        logging.info("Extracting audio from video...")
        audio_path = self.extract_audio_from_file(file_path)

        logging.info("Transcribing audio...")
        self.transcription = self.model.transcribe(audio_path)
        self.file_path = file_path

    def save_transcription(self, output_file=None):

        if self.transcription is None:
            raise ValueError(
                "No transcription available. Please transcribe audio first."
            )

        output_file = self.output_file(self.file_path, output_file, extension=".txt")

        logging.info("Saving transcription...")
        text = self.transcription["text"]
        # make line breaks after punctuation
        text = text.replace(". ", ".\n").replace("? ", "?\n").replace("! ", "!\n")
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text)

        logging.info(f"Transcription file '{output_file}' generated successfully.")

    def save_subtitles(self, output_file=None):
        """Main function to generate subtitles for a given video."""

        if self.transcription is None:
            raise ValueError(
                "No transcription available. Please transcribe audio first."
            )

        logging.info("Generating SRT file...")
        srt_content = self.generate_srt(self.transcription)

        output_file = self.output_file(self.file_path, output_file, extension=".srt")

        self.save_srt_file(output_file, srt_content)

        logging.info(f"Subtitle file '{output_file}' generated successfully.")

    def output_file(self, file_path, output_file=None, extension=".txt"):

        if output_file is None:
            output_file = os.path.splitext(file_path)[0] + extension
        else:
            dir, file = os.path.split(output_file)
            if not dir:
                dir, _ = os.path.splitext(file_path)
            os.makedirs(dir, exist_ok=True)

        return output_file

    def extract_audio_from_file(self, file_path):
        if self.is_video_file(file_path):
            return self.extract_audio_from_video(file_path)
        elif self.is_audio_file(file_path):
            return file_path
        else:
            raise ValueError(
                "Unsupported file type. Please provide a video or audio file."
            )

    def is_video_file(self, file_path):
        """Checks if a file is a video file based on its extension."""
        try:
            metadata = ffmpeg.probe(file_path, select_streams="v")["streams"][0]
            if metadata["codec_type"] == "video":
                return True
        except IndexError:
            return False

    def is_audio_file(self, file_path):
        """Checks if a file is an audio file based on its extension."""
        metadata = ffmpeg.probe(file_path, select_streams="a")["streams"][0]
        return metadata["codec_type"] == "audio"

    @staticmethod
    def extract_audio_from_video(video_path, audio_path="temp_audio.wav"):
        """Extracts audio using FFmpeg."""
        ffmpeg.input(video_path).output(audio_path, format="wav").run(
            overwrite_output=True
        )
        return audio_path

    @staticmethod
    def format_timedelta(seconds):
        """Formats a number of seconds into SRT time format (hh:mm:ss,ms)."""
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        milliseconds = int((td.total_seconds() - total_seconds) * 1000)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def generate_srt(self, transcription):
        """Generates SRT content from Whisper transcription output."""
        srt_content = ""
        for i, segment in enumerate(transcription["segments"]):
            start_time = self.format_timedelta(segment["start"])
            end_time = self.format_timedelta(segment["end"])
            text = segment["text"].strip()
            srt_content += f"{i + 1}\n{start_time} --> {end_time}\n{text}\n\n"
        return srt_content

    @staticmethod
    def save_srt_file(filename, srt_content):
        """Saves the generated SRT content to a file."""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(srt_content)
