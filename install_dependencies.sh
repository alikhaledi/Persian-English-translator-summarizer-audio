#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install FFmpeg based on OS
install_ffmpeg() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command_exists brew; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        echo "Installing FFmpeg using Homebrew..."
        brew install ffmpeg
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            # Debian/Ubuntu
            echo "Installing FFmpeg using apt..."
            sudo apt-get update
            sudo apt-get install -y ffmpeg
        elif command_exists yum; then
            # RHEL/CentOS
            echo "Installing FFmpeg using yum..."
            sudo yum install -y ffmpeg
        elif command_exists dnf; then
            # Fedora
            echo "Installing FFmpeg using dnf..."
            sudo dnf install -y ffmpeg
        else
            echo "Unsupported Linux distribution. Please install FFmpeg manually."
            exit 1
        fi
    else
        echo "Unsupported operating system. Please install FFmpeg manually."
        exit 1
    fi
}

# Function to install wkhtmltopdf based on OS
install_wkhtmltopdf() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command_exists brew; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        echo "Installing wkhtmltopdf using Homebrew..."
        brew install --cask wkhtmltopdf
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            # Debian/Ubuntu
            echo "Installing wkhtmltopdf using apt..."
            sudo apt-get update
            sudo apt-get install -y wkhtmltopdf
        elif command_exists yum; then
            # RHEL/CentOS
            echo "Installing wkhtmltopdf using yum..."
            sudo yum install -y wkhtmltopdf
        elif command_exists dnf; then
            # Fedora
            echo "Installing wkhtmltopdf using dnf..."
            sudo dnf install -y wkhtmltopdf
        else
            echo "Unsupported Linux distribution. Please install wkhtmltopdf manually."
            exit 1
        fi
    else
        echo "Unsupported operating system. Please install wkhtmltopdf manually."
        exit 1
    fi
}

# Function to install Python dependencies
install_python_deps() {
    if ! command_exists pip3; then
        echo "Installing pip..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install python3
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get install -y python3-pip
        fi
    fi
    
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
}

# Main installation process
echo "Starting installation process..."

# Install FFmpeg
echo "Checking FFmpeg installation..."
if ! command_exists ffmpeg; then
    echo "FFmpeg not found. Installing..."
    install_ffmpeg
else
    echo "FFmpeg is already installed."
fi

# Install wkhtmltopdf
echo "Checking wkhtmltopdf installation..."
if ! command_exists wkhtmltopdf; then
    echo "wkhtmltopdf not found. Installing..."
    install_wkhtmltopdf
else
    echo "wkhtmltopdf is already installed."
fi

# Install Python dependencies
echo "Installing Python dependencies..."
install_python_deps

echo "Installation completed successfully!"
echo "You can now run the video speed modification script." 