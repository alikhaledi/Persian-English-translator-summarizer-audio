# Persian-English Translator and Summarizer

A powerful application that translates Persian (Farsi) audio to English text, generates English audio, and creates intelligent summaries.

## Features

- 🎵 Download and process YouTube audio
- 🗣️ Transcribe Persian audio to text
- 🌍 Translate Persian text to English
- 🔊 Generate English audio from translated text
- 📝 Create intelligent summaries
- ⚡ Real-time processing with quality checks
- 💾 Save and reuse processed files
- 🎨 Beautiful dark-themed UI

## Screenshot

![Application Screenshot](screenshot.png)

## Prerequisites

- Python 3.10 or higher
- FFmpeg installed on your system
- OpenAI API key
- Conda environment manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alikhaledi/Persian-English-translator-summarizer-audio.git
cd Persian-English-translator-summarizer-audio
```

2. Create and activate the conda environment:
```bash
conda create -n audio python=3.10
conda activate audio
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key in your environment:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Running the Application

1. Activate the conda environment:
```bash
conda activate audio
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser and navigate to `http://localhost:8501`

## Usage

1. Enter a YouTube URL containing Persian audio
2. Choose whether to enable quality checks
3. Optionally enable "Use Saved Files" to reuse previously processed files
4. Click "Process Everything!" to start the translation process
5. View the results in the organized sections:
   - Original Persian audio
   - English audio translation
   - Persian transcription
   - English translation
   - Intelligent summary

## Output Files

All processed files are saved in the `output` directory:
- `{video_id}.mp3`: Original audio
- `{video_id}_farsi.txt`: Persian transcription
- `{video_id}_english.txt`: English translation
- `{video_id}_english.wav`: English audio
- `{video_id}_summary.txt`: Generated summary

## Quality Control

The application includes a quality control system that:
- Evaluates transcription accuracy
- Improves translation quality
- Ensures natural English output
- Maintains context and cultural references

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- OpenAI GPT-4 for translation and summarization
- Whisper for audio transcription
- Streamlit for the user interface
- FFmpeg for audio processing 