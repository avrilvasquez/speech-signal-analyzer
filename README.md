# Speech Signal Analyzer

A Python and Streamlit app that visualizes speech recordings through waveforms, spectrograms, and basic audio measurements.

I built this project to connect my Computer Science and Linguistics studies with hands-on speech signal processing.

## Live Demo

[Try the Speech Signal Analyzer](https://avril-speech-analyzer.streamlit.app/)

## Features

- Upload and play WAV recordings
- View recording duration, sample rate, and peak amplitude
- Plot amplitude over time as a waveform
- Explore frequency content over time with a spectrogram
- Average multichannel audio to mono for analysis

## Technologies

- Python
- Streamlit
- NumPy
- SciPy
- Matplotlib

## Run Locally

Clone the repository:

```bash
git clone https://github.com/avrilvasquez/speech-signal-analyzer.git
cd speech-signal-analyzer
```

Create and activate a virtual environment on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies and start the app:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

Upload a short WAV recording in the browser to explore its signal.

## Understanding the Graphs

**Waveform:** Shows amplitude over time. Near-flat sections can indicate pauses or quiet audio.

**Spectrogram:** Shows frequency content over time. Brighter colors represent stronger power relative to the recording's strongest spectrogram point.

## Limitations

- Supports WAV uploads only; some WAV encodings may not be readable.
- Designed for short recordings.
- Frequency display is capped at 8,000 Hz or the Nyquist frequency, whichever is lower.
- Peak amplitude is not a measurement of physical loudness.
- Spectrogram colors are relative to each recording, so they cannot directly compare absolute sound levels across files.
- Does not transcribe speech or identify words.

## Future Improvements

- Record audio directly in the app
- Compare two recordings
- Add adjustable spectrogram settings