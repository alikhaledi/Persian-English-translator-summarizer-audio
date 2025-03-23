# Persian-English Translator and Summarizer

An advanced AI-powered system for translating Persian audio to English text and generating summaries. This application uses OpenAI's GPT-4 and Whisper models to provide high-quality translations and intelligent content analysis.

## Features

- 🎵 High-quality audio processing
- 🗣️ Advanced Persian speech recognition
- 🌍 Context-aware Persian to English translation
- 🔊 Natural English audio generation
- 📝 Intelligent content summarization
- ⚡ Real-time processing with quality control
- 🎯 Customizable processing options

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- FFmpeg (for audio processing)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/alikhaledi/Persian-English-translator-summarizer-audio.git
   cd Persian-English-translator-summarizer-audio
   ```

2. Make the installation script executable:
   ```bash
   chmod +x install_dependencies.sh
   ```

3. Run the installation script:
   ```bash
   ./install_dependencies.sh
   ```

The installation script will:
- Create and activate a conda environment named 'audio'
- Install all required Python packages
- Set up FFmpeg if not already installed

### Manual Installation

If you prefer to install dependencies manually:

1. Create and activate a conda environment:
   ```bash
   conda create -n audio python=3.10
   conda activate audio
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - RHEL/CentOS: `sudo yum install ffmpeg`
   - Fedora: `sudo dnf install ffmpeg`

## Configuration

1. Create a `.env` file in the project directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Make the run script executable:
   ```bash
   chmod +x run.sh
   ```

2. Run the application:
   ```bash
   ./run.sh
   ```

The script will:
- Activate the conda environment
- Check for all required dependencies
- Verify the presence of your OpenAI API key
- Start the Streamlit web interface

## Usage

1. Enter a YouTube URL containing Persian audio
2. Enable/disable quality checks as needed
3. Click "Process Everything!" to start the translation process

The application will:
- Download and process the audio
- Transcribe Persian speech to text
- Translate the text to English
- Generate English audio
- Create a summary of the content

## Quality Control

The application includes a quality control system that:
- Evaluates transcription accuracy
- Checks translation quality
- Provides feedback on processing results
- Allows for multiple improvement iterations

## Output Files

The application generates several output files:
- `{video_id}.mp3`: Original audio file
- `{video_id}_farsi.txt`: Persian transcription
- `{video_id}_english.txt`: English translation
- `{video_id}_english.wav`: English audio
- `{video_id}_summary.txt`: Content summary

## Notes

- The application requires an active internet connection
- Processing time depends on the audio length and quality settings
- Quality checks may increase processing time but improve accuracy
- All temporary files are automatically cleaned up after processing

## License

Feel free to use and modify this application as needed. 