from __future__ import annotations

from pathlib import Path
from typing import Dict
import os

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).parent / ".matplotlib_cache"))

import matplotlib.pyplot as plt
import numpy as np


def _load_audio(audio_path: str | Path, target_sr: int = 16000) -> tuple[np.ndarray, int]:
    """Load audio with librosa when available, falling back to soundfile."""
    path = str(audio_path)
    try:
        import librosa

        y, sr = librosa.load(path, sr=target_sr, mono=True)
        return np.asarray(y, dtype=float), int(sr)
    except Exception:
        import soundfile as sf

        data, sr = sf.read(path)
        if data.ndim > 1:
            data = data.mean(axis=1)
        data = np.asarray(data, dtype=float)
        if sr != target_sr:
            try:
                from scipy.signal import resample_poly

                gcd = np.gcd(sr, target_sr)
                data = resample_poly(data, target_sr // gcd, sr // gcd)
                sr = target_sr
            except Exception:
                pass
        return data, int(sr)


def extract_audio_features(audio_path: str | Path) -> Dict[str, float]:
    y, sr = _load_audio(audio_path)
    if y.size == 0:
        return {
            "pause_ratio": 1.0,
            "rms_energy": 0.0,
            "zero_crossing_rate": 0.0,
            "duration_sec": 0.0,
        }

    duration = float(len(y) / sr)
    rms = float(np.sqrt(np.mean(np.square(y))))
    threshold = max(rms * 0.35, 0.01)
    pause_ratio = float(np.mean(np.abs(y) < threshold))
    zero_crossings = np.mean(np.abs(np.diff(np.signbit(y))))

    return {
        "pause_ratio": round(pause_ratio, 4),
        "rms_energy": round(rms, 4),
        "zero_crossing_rate": round(float(zero_crossings), 4),
        "duration_sec": round(duration, 2),
    }


def save_waveform(audio_path: str | Path, output_path: str | Path) -> str:
    y, sr = _load_audio(audio_path)
    times = np.arange(len(y)) / sr if y.size else np.array([0])
    samples = y if y.size else np.array([0])

    plt.figure(figsize=(10, 3.4), dpi=140)
    plt.plot(times, samples, color="#2e8ac8", linewidth=1)
    plt.title("Audio Waveform", fontsize=10)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.ylim(-1.05, 1.05)
    plt.grid(alpha=0.15)
    plt.tight_layout()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, facecolor="white")
    plt.close()
    return str(output)
