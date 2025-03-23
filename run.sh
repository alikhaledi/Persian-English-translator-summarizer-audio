#!/bin/bash

echo "🚀 Starting the application..."
echo "Choose mode (press 't' for terminal, 'u' for UI, or wait 5 seconds for UI):"

# Countdown timer
for i in {5..1}; do
    echo -ne "\rStarting UI mode in $i seconds... (press 't' for terminal, 'u' for UI)"
    read -t 1 -n 1 mode
    if [ ! -z "$mode" ]; then
        echo
        break
    fi
done

# If no input received or user pressed 'u', run UI
if [ -z "$mode" ] || [ "$mode" = "u" ]; then
    echo "Starting UI mode..."
    streamlit run app.py
# If user pressed 't', run terminal mode
elif [ "$mode" = "t" ]; then
    echo "Starting terminal mode..."
    python3 Farsi_audio_to_English_transcript.py
else
    echo "Invalid input. Starting UI mode..."
    streamlit run app.py
fi 