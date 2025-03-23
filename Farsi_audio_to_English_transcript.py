import os
import re
import base64
from openai import OpenAI
from pydub import AudioSegment
import yt_dlp
import time

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def download_youtube_audio(url, output_path):
    print(f"🔁 Downloading audio from YouTube: {url}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path.replace('.mp3', ''),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"✅ Downloaded audio to {output_path}")

def split_audio(audio_path, chunk_length_ms=600000):
    audio = AudioSegment.from_mp3(audio_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = f"{audio_path[:-4]}_chunk_{i//chunk_length_ms}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks

def evaluate_transcription_quality(text):
    """
    Evaluates the quality of transcription using GPT-4.
    Returns a quality score (0-100) and specific issues found.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a Persian language expert evaluating transcription quality. Analyze the text and provide:
1. A quality score (0-100)
2. List of specific issues found
3. Whether the text needs improvement

Format your response as:
SCORE: [number]
ISSUES: [list of issues]
NEEDS_IMPROVEMENT: [yes/no]"""
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    
    result = response.choices[0].message.content
    score = int(re.search(r'SCORE:\s*(\d+)', result).group(1))
    issues = re.search(r'ISSUES:\s*(.*?)(?=NEEDS_IMPROVEMENT:|$)', result, re.DOTALL).group(1).strip()
    needs_improvement = re.search(r'NEEDS_IMPROVEMENT:\s*(yes|no)', result).group(1).lower() == 'yes'
    
    return score, issues, needs_improvement

def improve_transcription(text):
    """
    Improves transcription quality using GPT-4 with specific focus on issues found.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a Persian language expert improving transcription quality. Your task is to:
1. Correct any transcription errors
2. Fix punctuation and spacing
3. Ensure proper Persian grammar and sentence structure
4. Maintain the original meaning and tone
5. Preserve any specific terminology or names
6. Make the text flow naturally in Persian
7. Fix any inconsistencies or unclear parts
8. Ensure proper paragraph structure

Provide only the improved text without any explanations or additional formatting."""
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content

def transcribe_farsi(audio_path, max_retries=3, quality_check=True):
    """
    Transcribes Farsi audio to Farsi text using whisper-1 and enhances it with GPT-4.
    Includes quality feedback loop for continuous improvement if quality_check is True.
    """
    file_size = os.path.getsize(audio_path)
    all_text = []

    def transcribe(file_path):
        with open(file_path, "rb") as f:
            return client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text",
                language="fa"
            )

    if file_size > 25 * 1024 * 1024:
        print("🔪 Splitting audio into smaller chunks...")
        chunks = split_audio(audio_path)
        for chunk_path in chunks:
            print(f"📝 Transcribing chunk: {chunk_path}")
            text = transcribe(chunk_path)
            all_text.append(text)
            os.remove(chunk_path)
    else:
        print(f"📝 Transcribing full audio: {audio_path}")
        text = transcribe(audio_path)
        all_text.append(text)

    # Combine all transcribed text
    raw_text = "\n".join([t.text if hasattr(t, "text") else str(t) for t in all_text])
    
    if not quality_check:
        print("⚡ Skipping quality check for faster processing")
        return raw_text
    
    # Quality feedback loop for transcription
    current_text = raw_text
    for attempt in range(max_retries):
        print(f"\n🔄 Transcription Quality Check (Attempt {attempt + 1}/{max_retries})")
        score, issues, needs_improvement = evaluate_transcription_quality(current_text)
        print(f"📊 Quality Score: {score}/100")
        
        if not needs_improvement or score >= 90:
            print("✅ Transcription quality is satisfactory!")
            break
            
        print(f"⚠️ Issues found: {issues}")
        print("🔄 Attempting to improve transcription...")
        current_text = improve_transcription(current_text)
        time.sleep(1)  # Rate limiting
    
    return current_text

def evaluate_translation_quality(farsi_text, english_text):
    """
    Evaluates the quality of translation using GPT-4.
    Returns a quality score (0-100) and specific issues found.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a Persian-English translation expert evaluating translation quality. Analyze the translation and provide:
1. A quality score (0-100)
2. List of specific issues found
3. Whether the translation needs improvement

Consider:
- Accuracy of meaning
- Natural English flow
- Cultural context preservation
- Technical accuracy
- Consistency
- Completeness

Format your response as:
SCORE: [number]
ISSUES: [list of issues]
NEEDS_IMPROVEMENT: [yes/no]"""
            },
            {
                "role": "user",
                "content": f"Original Persian text:\n{farsi_text}\n\nEnglish translation:\n{english_text}"
            }
        ]
    )
    
    result = response.choices[0].message.content
    score = int(re.search(r'SCORE:\s*(\d+)', result).group(1))
    issues = re.search(r'ISSUES:\s*(.*?)(?=NEEDS_IMPROVEMENT:|$)', result, re.DOTALL).group(1).strip()
    needs_improvement = re.search(r'NEEDS_IMPROVEMENT:\s*(yes|no)', result).group(1).lower() == 'yes'
    
    return score, issues, needs_improvement

def improve_translation(farsi_text, english_text):
    """
    Improves translation quality using GPT-4 with specific focus on issues found.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a professional Persian-English translator improving translation quality. Your task is to:
1. Ensure accurate meaning preservation
2. Improve natural English flow
3. Maintain cultural context
4. Fix any technical inaccuracies
5. Ensure consistency throughout
6. Complete any missing parts
7. Use appropriate English expressions
8. Maintain the original tone and style

Provide only the improved English translation without any explanations or additional formatting."""
            },
            {
                "role": "user",
                "content": f"Original Persian text:\n{farsi_text}\n\nCurrent English translation:\n{english_text}"
            }
        ]
    )
    return response.choices[0].message.content

def translate_farsi_to_english(farsi_text, max_retries=3, quality_check=True):
    """
    Translates Farsi transcript into concise, clear English using GPT-4.
    Includes quality feedback loop for continuous improvement if quality_check is True.
    """
    print("🌍 Translating to English with GPT-4...")
    
    # Initial translation
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a professional Persian-English translator specializing in clear, concise translations. Your goal is to:
1. Translate the text into direct, clear English
2. Focus on the main points and key messages
3. Remove unnecessary verbosity while preserving meaning
4. Use natural English expressions
5. Maintain the original tone and intent
6. Break complex sentences into simpler ones
7. Preserve proper nouns and specific terminology

Guidelines:
- Be direct and to the point
- Use active voice when possible
- Keep sentences concise
- Maintain professional tone
- Preserve cultural context
- Ensure logical flow

Provide only the translated text without any explanations or additional formatting."""
            },
            {
                "role": "user",
                "content": farsi_text
            }
        ]
    )
    current_translation = response.choices[0].message.content
    
    if not quality_check:
        print("⚡ Skipping quality check for faster processing")
        return current_translation
    
    # Quality feedback loop for translation
    for attempt in range(max_retries):
        print(f"\n🔄 Translation Quality Check (Attempt {attempt + 1}/{max_retries})")
        score, issues, needs_improvement = evaluate_translation_quality(farsi_text, current_translation)
        print(f"📊 Quality Score: {score}/100")
        
        if not needs_improvement or score >= 90:
            print("✅ Translation quality is satisfactory!")
            break
            
        print(f"⚠️ Issues found: {issues}")
        print("🔄 Attempting to improve translation...")
        current_translation = improve_translation(farsi_text, current_translation)
        time.sleep(1)  # Rate limiting
    
    return current_translation

def generate_english_audio_gpt4o(text, output_path, voice="alloy"):
    print("🔊 Generating English speech...")
    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": voice, "format": "wav"},
        messages=[
            {
                "role": "user",
                "content": f"Please read this exactly as written:\n\n{text}"
            }
        ]
    )
    wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    with open(output_path, "wb") as f:
        f.write(wav_bytes)
    print(f"✅ Audio saved to {output_path}")

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Saved to {filename}")

def extract_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=56WsSzrx98A"
    video_id = extract_video_id(youtube_url)
    if not video_id:
        print("❌ Invalid YouTube URL")
        exit(1)

    try:
        audio_file = f"{video_id}.mp3"
        farsi_transcript_file = f"{video_id}_farsi.txt"
        english_transcript_file = f"{video_id}_english.txt"
        english_audio_file = f"{video_id}_english.wav"

        # Step 1: Download
        download_youtube_audio(youtube_url, audio_file)

        # Step 2: Transcribe (Farsi) with optional quality feedback
        farsi_text = transcribe_farsi(audio_file, quality_check=True)  # Set to False for faster processing
        save_to_file(farsi_text, farsi_transcript_file)

        # Step 3: Translate with optional quality feedback
        english_text = translate_farsi_to_english(farsi_text, quality_check=True)  # Set to False for faster processing
        save_to_file(english_text, english_transcript_file)

        # Step 4: English audio
        generate_english_audio_gpt4o(english_text, english_audio_file)

        # Cleanup
        os.remove(audio_file)

        print("\n🎉 All done!")
        print(f"📄 English text: {english_transcript_file}")
        print(f"🔊 English audio: {english_audio_file}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
