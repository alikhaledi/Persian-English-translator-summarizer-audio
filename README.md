# Video Speed Modification Script

This script allows you to modify the speed of a video file by creating three segments:
1. First 30 seconds at normal speed
2. Middle section (30s to 3m30s) at 3x speed
3. Remaining duration at normal speed

## Prerequisites

The script requires FFmpeg and Python 3 to be installed. You can install all dependencies automatically using the installation script.

## Installation

1. Clone this repository or download the files
2. Make the installation script executable:
   ```bash
   chmod +x install_dependencies.sh
   ```
3. Run the installation script:
   ```bash
   ./install_dependencies.sh
   ```

The installation script will:
- Detect your operating system (macOS or Linux)
- Install FFmpeg if not already installed
- Install Python dependencies from requirements.txt

### Manual Installation

If you prefer to install dependencies manually:

#### FFmpeg Installation
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt-get install ffmpeg`
- RHEL/CentOS: `sudo yum install ffmpeg`
- Fedora: `sudo dnf install ffmpeg`

#### Python Dependencies
```bash
pip3 install -r requirements.txt
```

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
- Check for all required dependencies
- Verify the presence of your OpenAI API key
- Install any missing Python packages
- Start the Streamlit web interface

## Usage

1. Place your video file (named `Recording_for_Ehsan.mov`) in the same directory as the script
2. Make the script executable:
   ```bash
   chmod +x change_speed.sh
   ```
3. Run the script:
   ```bash
   ./change_speed.sh
   ```

The script will create a new file named `Recording_for_Ehsan_modified_speed.mov` in the same directory.

## How it Works

The script:
1. Splits the video into three parts
2. Applies different speed modifications to each part
3. Concatenates the parts back together
4. Cleans up temporary files automatically

## Notes

- The script requires FFmpeg to be installed and accessible from the command line
- The input video must be named `Recording_for_Ehsan.mov`
- The output will be saved as `Recording_for_Ehsan_modified_speed.mov`
- The script will automatically overwrite any existing output file without asking for confirmation

## License

Feel free to use and modify this script as needed. 