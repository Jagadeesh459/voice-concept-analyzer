# Code Documentation

## Project Title

Voice-Based Concept Understanding Analyser

## Purpose

This project evaluates a student's spoken conceptual explanation using a Streamlit web interface. The system accepts an audio upload, optionally accepts a student transcription, extracts audio-level features, computes text-based metrics when transcription is available, calculates a final understanding score, displays the result, and generates a downloadable PDF report.

The deployed free-tier version uses a lightweight architecture so it can run within Render memory limits. Automatic Whisper transcription is optional in the code, but not required by the deployed dependency set.

## User Workflow

1. The user opens the Streamlit application.
2. The user reviews or edits the reference concept.
3. The user uploads a student audio file.
4. The user may paste the student transcription.
5. The user clicks `Analyze Concept Understanding`.
6. The application calculates audio and text metrics.
7. The application displays the transcript/evaluation summary.
8. The user can download a PDF report.

## Architecture Overview

```text
app.py
  -> audio_utils.py
  -> speech_to_text.py
  -> semantic_eval.py
  -> scoring_engine.py
  -> report_generator.py
```

The project is intentionally modular. The Streamlit file handles interface and workflow orchestration, while each helper module owns a specific part of the analysis pipeline.

## File-by-File Explanation

### `app.py`

This is the main Streamlit application.

Main responsibilities:

- Configures the Streamlit page.
- Loads custom CSS from `style.css`.
- Displays the reference concept input.
- Handles student audio upload.
- Provides optional student transcription input.
- Runs the analysis pipeline.
- Stores results in Streamlit session state.
- Displays final metrics, score, understanding level, waveform, and PDF download.

Important functions:

- `load_css()` loads the app styling.
- `init_state()` initializes result values in `st.session_state`.
- `save_uploaded_file()` saves uploaded audio temporarily inside `outputs/`.
- `run_analysis()` coordinates transcription, audio feature extraction, similarity, scoring, waveform generation, and PDF creation.
- `render_results()` displays final output after analysis.
- `main()` builds the Streamlit UI.

### `audio_utils.py`

This module handles audio processing.

Main responsibilities:

- Loads uploaded audio using `soundfile`.
- Converts stereo audio to mono.
- Computes audio features:
  - duration
  - pause ratio
  - RMS energy
  - zero crossing rate
- Saves waveform visualization as an image.

Important functions:

- `_load_audio()` loads the audio file and returns samples plus sample rate.
- `extract_audio_features()` calculates audio-level metrics.
- `save_waveform()` creates and saves the waveform chart using Matplotlib.

### `speech_to_text.py`

This module contains optional speech-to-text support.

Main responsibilities:

- Uses Whisper if it is installed in the environment.
- Returns an empty result if Whisper is unavailable.

In the free Render deployment, Whisper is not installed because it requires heavy dependencies such as `torch`, which can exceed free memory limits.

Important function:

- `speech_to_text()` tries to transcribe audio using Whisper and otherwise returns an empty string.

### `semantic_eval.py`

This module computes semantic similarity between the student explanation and the reference concept.

Main responsibilities:

- Defines the default reference concept.
- Tokenizes input text.
- Computes cosine similarity using a lightweight bag-of-words method.

The original project design can support Sentence-BERT, but the deployed lightweight version avoids large model dependencies for free hosting.

Important functions:

- `_tokenize()` extracts lowercase words from text.
- `_bag_of_words_similarity()` calculates cosine similarity.
- `semantic_similarity()` returns a normalized similarity score from `0.0` to `1.0`.

### `scoring_engine.py`

This module calculates language and understanding metrics.

Main responsibilities:

- Detects filler words.
- Computes filler word ratio.
- Combines semantic and audio metrics into a final score.
- Classifies the understanding level.

Important functions:

- `filler_word_ratio()` counts filler words in the transcript.
- `evaluate_understanding()` calculates final score and returns:
  - score
  - understanding level
  - display color

Scoring categories:

```text
80-100  Strong Understanding
50-79   Moderate Understanding
0-49    Poor Understanding
```

### `report_generator.py`

This module creates the downloadable PDF report.

Main responsibilities:

- Builds a structured PDF using ReportLab.
- Adds:
  - reference concept
  - student transcription or audio-only note
  - waveform image
  - evaluation metric table
  - qualitative feedback

Important function:

- `generate_pdf_report()` writes the PDF report and returns its file path.

### `style.css`

This file contains custom CSS for the Streamlit interface.

Main responsibilities:

- Creates the dark visual theme.
- Styles result panels, metric tiles, upload area, buttons, and labels.
- Improves spacing, typography, and responsive layout.

### `.streamlit/config.toml`

This file configures Streamlit.

Main settings:

- Uses a dark theme.
- Disables usage statistics.
- Runs in headless mode for deployment.
- Sets toolbar mode to minimal so developer controls do not appear in the app.

### `requirements.txt`

This file lists Python packages needed by the lightweight deployment version:

```text
streamlit
soundfile
matplotlib
reportlab
numpy
```

Heavy ML packages were removed for free cloud deployment:

```text
torch
openai-whisper
sentence-transformers
transformers
librosa
```

### `packages.txt`

This file is used by Render to install system packages.

Current package:

```text
ffmpeg
```

### `Procfile`

This file defines the web process command for Render-compatible deployment.

### `render.yaml`

This file defines Render deployment configuration as infrastructure-as-code.

It includes:

- service type
- Python environment
- free plan
- build command
- start command

### `runtime.txt`

This file pins the Python version for deployment:

```text
python-3.11.9
```

### `.gitignore`

This file prevents generated/local files from being committed.

Ignored examples:

- Python cache files
- local virtual environments
- generated outputs
- Matplotlib cache
- environment files

## Analysis Logic

### Audio Metrics

The app extracts these values from uploaded audio:

- `pause_ratio`: estimated percentage of low-energy samples.
- `rms_energy`: average signal energy, used as a confidence indicator.
- `zero_crossing_rate`: rate of signal sign changes.
- `duration_sec`: audio duration in seconds.

### Text Metrics

If a transcript is available, the app calculates:

- `semantic_similarity`: similarity between transcript and reference concept.
- `filler_ratio`: filler word count divided by total word count.

If no transcript is provided, these text metrics are set to `0.0`, and the app performs audio-only evaluation.

### Final Score

The scoring engine combines:

- semantic similarity
- filler word ratio
- pause ratio
- RMS energy

The final output includes:

- numeric score out of 100
- qualitative understanding level
- color-coded result label

## Lightweight Deployment Note

The original system design includes automatic speech-to-text using Whisper and semantic embedding comparison using Sentence-BERT. Those features require large dependencies and model memory.

For free Render deployment, the app uses a lightweight mode:

- The user may paste transcription manually.
- Audio analysis still runs.
- Waveform visualization still runs.
- Scoring and PDF reporting still run.
- No heavy ML models are loaded in the cloud environment.

This avoids memory-limit crashes while preserving the main evaluation workflow.

## Local Run Instructions

```powershell
cd "C:\Users\Nachi\OneDrive\Desktop\New folder"
.\vbcu_env\Scripts\streamlit.exe run app.py
```

Then open:

```text
http://localhost:8501
```

## Render Deployment Settings

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT --server.headless=true --browser.gatherUsageStats=false --client.toolbarMode=minimal
```

No custom environment variables are required. Render automatically provides `$PORT`.

## Known Limitations

- Free deployment does not include automatic Whisper transcription.
- Free deployment does not include Sentence-BERT embeddings.
- MP3/M4A support can depend on server audio decoding support.
- Generated reports and waveform images are temporary server files.

## Future Enhancements

- Add external API-based transcription to avoid local Whisper memory usage.
- Add external embedding API for stronger semantic scoring.
- Store reports and sessions in a database.
- Add user login and progress tracking.
- Add multi-concept evaluation support.
- Add multilingual transcription and evaluation.
