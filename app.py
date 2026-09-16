import io

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from scipy.io import wavfile
from scipy.signal import spectrogram

st.set_page_config(page_title="Speech Signal Analyzer", page_icon="🎙️")

st.title("🎙️ Speech Signal Analyzer")
st.write(
    "Explore a speech recording through its waveform, "
    "spectrogram, and basic audio measurements."
)

uploaded_file = st.file_uploader("Upload a WAV recording", type=["wav"])

if uploaded_file is None:
    st.info("Upload a short WAV recording to get started.")
    st.stop()

audio_bytes = uploaded_file.getvalue()
st.audio(audio_bytes, format="audio/wav")

try:
    sample_rate, raw_audio = wavfile.read(io.BytesIO(audio_bytes))
except Exception:
    st.error("Unable to read this recording. Try another WAV file.")
    st.stop()

if sample_rate <= 0 or raw_audio.size == 0:
    st.error("This file contains no usable audio.")
    st.stop()

# Convert samples to floating point using the file's amplitude scale.
if raw_audio.dtype == np.uint8:
    audio = (raw_audio.astype(np.float64) - 128) / 128
elif np.issubdtype(raw_audio.dtype, np.signedinteger):
    scale = float(-np.iinfo(raw_audio.dtype).min)
    audio = raw_audio.astype(np.float64) / scale
elif np.issubdtype(raw_audio.dtype, np.floating):
    audio = raw_audio.astype(np.float64)
else:
    st.error("This WAV file uses an unsupported sample format.")
    st.stop()

# Average stereo channels for analysis.
if audio.ndim == 2:
    audio = audio.mean(axis=1)
    st.caption("Channels are averaged to mono for analysis.")

if not np.all(np.isfinite(audio)):
    st.error("The recording contains invalid sample values.")
    st.stop()

if len(audio) < 32:
    st.error("This recording is too short. Upload a longer clip.")
    st.stop()

duration = len(audio) / sample_rate
peak_amplitude = np.max(np.abs(audio))

col1, col2, col3 = st.columns(3)
col1.metric("Duration", f"{duration:.2f} seconds")
col2.metric("Sample rate", f"{sample_rate:,} Hz")
col3.metric("Peak amplitude", f"{peak_amplitude:.3f}")

st.caption(
    "Peak amplitude is the largest absolute sample value in the "
    "analyzed signal. It is not a measurement of physical loudness."
)

st.subheader("Waveform")
st.write(
    "The waveform shows how the signal's amplitude changes over time."
)

time = np.arange(len(audio)) / sample_rate

fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(time, audio, color="#2563eb", linewidth=0.6)
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Amplitude")
ax.set_xlim(0, duration)
ax.grid(alpha=0.2)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.subheader("Spectrogram")
st.write(
    "The spectrogram shows how frequency content changes over time. "
    "Brighter colors indicate stronger energy."
)

# Use an approximately 25-millisecond analysis window.
window_size = min(len(audio), max(32, int(sample_rate * 0.025)))

frequencies, times, power = spectrogram(
    audio,
    fs=sample_rate,
    window="hann",
    nperseg=window_size,
    noverlap=window_size // 2,
)

# Display power relative to the strongest point, over an 80 dB range.
reference = max(float(power.max()), np.finfo(float).tiny)
relative_power = np.maximum(power / reference, 1e-8)
power_db = 10 * np.log10(relative_power)

fig, ax = plt.subplots(figsize=(10, 4))
mesh = ax.pcolormesh(
    times,
    frequencies,
    power_db,
    shading="auto",
    cmap="magma",
    vmin=-80,
    vmax=0,
)
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Frequency (Hz)")
ax.set_ylim(0, min(8000, sample_rate / 2))
fig.colorbar(mesh, ax=ax, label="Power relative to peak (dB)")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.caption(
    "The frequency display is capped at 8,000 Hz. "
    "Colors are relative to this recording, not calibrated sound levels."
)

if peak_amplitude == 0:
    st.warning("This recording is silent.")