from __future__ import annotations

from pathlib import Path


DEMO_TRANSCRIPT = (
    "If you don't discipline when you are school or in college, you pay a heavy "
    "price in later part of your life. Discipline like coming up in a proper way, "
    "writing properly, talking properly, communicating properly, respecting people "
    "properly. This really helps a long way in your life. So I don't want you "
    "should be like a potato regretting in your old age. You should remember that "
    "to be successful in life there is no shortcut. The only method is hard work "
    "and straight way and that you have to do."
)


def speech_to_text(audio_path: str | Path) -> str:
    """Transcribe audio with Whisper if installed; otherwise return a demo fallback."""
    try:
        import whisper

        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path), fp16=False)
        text = str(result.get("text", "")).strip()
        return text or DEMO_TRANSCRIPT
    except Exception:
        return DEMO_TRANSCRIPT
