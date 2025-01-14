from flask import Flask, render_template, request, jsonify
import os
import numpy as np
import librosa
from librosa.display import specshow
import matplotlib.pyplot as plt
import speech_recognition as sr
from pydub import AudioSegment
import io
import base64

# Initialize Flask app
app = Flask(__name__)

# Function to convert matplotlib plots to base64

def plot_to_base64(fig):
    """Convert matplotlib plot to a base64 string for embedding in HTML."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return img_base64

# Function to transcribe audio

def transcribe_audio(file_path):
    """Transcribe the audio to text."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)

# Route to render homepage

@app.route('/')
def index():
    return render_template('index.html')

# Route to process uploaded audio file

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    # Ensure 'uploads' directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    file = request.files['file']
    raw_audio_path = os.path.join('uploads', file.filename)
    file.save(raw_audio_path)

    try:
        # Convert audio to WAV format
        audio = AudioSegment.from_file(raw_audio_path)
        wav_audio_path = raw_audio_path.replace(".webm", ".wav")
        audio.export(wav_audio_path, format="wav")
    except Exception as e:
        return jsonify({'error': f'Error processing audio: {e}'}), 500

    try:
        # Transcribe audio
        transcription = transcribe_audio(wav_audio_path)

        # Extract audio signal, sampling rate, and features
        signal, sampling_rate = librosa.load(wav_audio_path, sr=16000)

        # Generate waveform plot
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(np.linspace(0, len(signal) / sampling_rate, len(signal)), signal)
        ax.set_title("Audio Signal")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        waveform_img = plot_to_base64(fig)
        plt.close(fig)

        # Generate MFCC heatmap
        mfcc = librosa.feature.mfcc(y=signal, sr=sampling_rate, n_mfcc=13)
        fig, ax = plt.subplots(figsize=(10, 4))
        specshow(mfcc, sr=sampling_rate, x_axis="time", ax=ax, cmap="viridis")
        ax.set_title("MFCC Heatmap")
        ax.set_xlabel("Time")
        ax.set_ylabel("MFCC Coefficients")
        mfcc_img = plot_to_base64(fig)
        plt.close(fig)

        # Generate Spectrogram
        fig, ax = plt.subplots(figsize=(10, 4))
        S = librosa.amplitude_to_db(np.abs(librosa.stft(signal)), ref=np.max)
        specshow(S, sr=sampling_rate, x_axis="time", y_axis="hz", ax=ax, cmap="magma")
        ax.set_title("Spectrogram")
        ax.set_xlabel("Time")
        ax.set_ylabel("Frequency (Hz)")
        spectrogram_img = plot_to_base64(fig)
        plt.close(fig)

        # Generate comparison: Linear vs Log Scales
        fig, axs = plt.subplots(2, 1, figsize=(10, 6), constrained_layout=True)
        axs[0].plot(np.abs(S[0]), label="Linear Scale")
        axs[0].set_title("Linear Scale")
        axs[1].plot(np.log1p(np.abs(S[0])), label="Log Scale")
        axs[1].set_title("Log Scale")
        axs[0].set_ylabel("Amplitude")
        axs[1].set_ylabel("Log-Amplitude")
        axs[1].set_xlabel("Frequency Bins")
        log_comparison_img = plot_to_base64(fig)
        plt.close(fig)

        return jsonify({
            'transcription': transcription,
            'waveform_img': waveform_img,
            'mfcc_img': mfcc_img,
            'spectrogram_img': spectrogram_img,
            'log_comparison_img': log_comparison_img
        })
    except Exception as e:
        return jsonify({'error': f'Error extracting features: {e}'}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
