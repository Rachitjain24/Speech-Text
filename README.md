# Speech-to-Text Visualization Web Application

## Overview
This is a Flask-based web application that processes audio files to:
1. Transcribe speech to text using Google Speech Recognition.
2. Visualize key audio features such as:
   - **Waveform**
   - **MFCC Heatmap**
   - **Spectrogram**
   - **Comparison of Linear and Log Scales**

## Features
- **Speech Transcription**: Converts uploaded audio files into text.
- **Waveform Visualization**: Displays the amplitude of the audio signal over time.
- **MFCC Heatmap**: Visualizes Mel-Frequency Cepstral Coefficients (MFCCs) for the uploaded audio.
- **Spectrogram**: Shows the frequency content of the audio over time.
- **Linear vs Log Scale Comparison**: Compares raw amplitude and logarithmic scaling of the frequency bins.

## Prerequisites

### Software Requirements:
- Python 3.7 or higher
- Flask

### Python Libraries:
Install the required libraries using pip:

```bash
pip install flask librosa matplotlib speechrecognition pydub numpy
```

### Additional Tools:
- **FFmpeg**: Required for audio processing using `pydub`.
  - [Installation guide](https://ffmpeg.org/download.html).

## How to Run the Application

1. Clone or download this repository to your local machine.
2. Install the required Python libraries (as listed above).
3. Ensure FFmpeg is installed and added to your system’s PATH.
4. Run the Flask application:

```bash
python app.py
```

5. Open your web browser and navigate to:

```
http://127.0.0.1:5000/
```

## How It Works

### Workflow:
1. **Upload Audio File**:
   - The user uploads an audio file in `.webm` or other supported formats.
2. **Preprocessing**:
   - The audio file is converted to `.wav` format for further processing.
   - The signal is sampled at 16 kHz.
3. **Feature Extraction**:
   - **Waveform**: Extracted and plotted.
   - **MFCC**: Computed using `librosa.feature.mfcc()` and visualized as a heatmap.
   - **Spectrogram**: Generated using Short-Time Fourier Transform (STFT) and visualized.
   - **Linear vs Log Scale**: Frequency bins are compared on linear and log scales.
4. **Speech-to-Text**:
   - Transcription is performed using the `speech_recognition` library.
5. **Visualization**:
   - Processed features and transcription are returned as JSON and displayed in the browser.

## API Endpoints

### `/`
- **Method**: `GET`
- **Description**: Renders the main page for uploading and visualizing audio files.

### `/process_audio`
- **Method**: `POST`
- **Description**: Processes the uploaded audio file and returns transcription and visualizations.
- **Request Parameters**:
  - `file`: Audio file to be uploaded.
- **Response**:
  - `transcription`: The transcribed text.
  - `waveform_img`: Base64 string of the waveform image.
  - `mfcc_img`: Base64 string of the MFCC heatmap.
  - `spectrogram_img`: Base64 string of the spectrogram.
  - `log_comparison_img`: Base64 string comparing linear and log frequency bins.

## Code Explanation

### Key Functions:
1. **`plot_to_base64(fig)`**:
   - Converts matplotlib figures to base64 strings for embedding in HTML.

2. **`transcribe_audio(file_path)`**:
   - Transcribes the uploaded audio file using Google Speech Recognition.

3. **Feature Extraction**:
   - **Waveform**: Plotted using `matplotlib`.
   - **MFCC**: Extracted with `librosa.feature.mfcc()` and displayed as a heatmap.
   - **Spectrogram**: Generated with `librosa.stft()` and visualized in decibels.
   - **Linear vs Log Scale Comparison**: Compares raw amplitudes and logarithmic scaling of frequency bins.

### Directory Management:
- Ensures `uploads` directory exists to store temporary audio files.

## Example Request

### Using `curl`:
```bash
curl -X POST -F "file=@path_to_audio.webm" http://127.0.0.1:5000/process_audio
```

## Troubleshooting

1. **`speech_recognition` errors**:
   - Ensure you have an active internet connection for Google Speech Recognition.

2. **FFmpeg issues**:
   - Verify FFmpeg is installed and added to your PATH.

3. **Library compatibility**:
   - Use Python 3.7 or higher and ensure all required libraries are installed.

## Screenshots

1. **Waveform Visualization**
   - Displays the amplitude over time.
2. **MFCC Heatmap**
   - Visual representation of MFCCs.
3. **Spectrogram**
   - Frequency content visualized over time.
4. **Linear vs Log Comparison**
   - Highlights the difference between linear and logarithmic scales.

## Future Enhancements
- Add support for real-time audio recording in the browser.
- Include advanced transcription options using pre-trained models like Wav2Vec2.
- Optimize the visualization process for larger audio files.

## License
This project is licensed under the MIT License.

