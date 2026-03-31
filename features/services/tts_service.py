"""Server-side TTS helpers for LexiCode."""
from __future__ import annotations

import asyncio
from typing import Tuple

try:
    import edge_tts
except Exception:
    edge_tts = None

TTS_VOICE_MAP = {
    'en': {'female': 'en-US-JennyNeural', 'male': 'en-US-GuyNeural'},
    'tr': {'female': 'tr-TR-EmelNeural', 'male': 'tr-TR-AhmetNeural'},
}


def clean_tts_text(text: str) -> str:
    cleaned = ' '.join(str(text or '').split()).strip()
    cleaned = (
        cleaned
        .replace('C++', 'C plus plus')
        .replace('C#', 'C sharp')
        .replace('/', ' veya ')
    )
    return cleaned[:700]


def pick_server_tts_voice(language: str = 'en-US', gender: str = 'female') -> str:
    prefix = 'tr' if str(language or '').lower().startswith('tr') else 'en'
    desired = 'male' if str(gender or '').lower() == 'male' else 'female'
    return TTS_VOICE_MAP[prefix][desired]


def edge_rate_from_value(rate, language: str = 'en-US') -> str:
    default_rate = 0.92 if str(language or '').lower().startswith('tr') else 0.86
    try:
        numeric_rate = float(rate)
    except (TypeError, ValueError):
        numeric_rate = default_rate
    pct = max(-50, min(50, round((numeric_rate - 1.0) * 100)))
    return f'{pct:+d}%'


async def _synthesize_tts_audio(text: str, voice: str, rate: str) -> bytes:
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    audio = bytearray()
    async for chunk in communicate.stream():
        if chunk.get('type') == 'audio':
            audio.extend(chunk['data'])
    return bytes(audio)


def generate_tts_audio(text: str, language: str = 'en-US', gender: str = 'female', rate=None) -> Tuple[bytes, str]:
    if edge_tts is None:
        raise RuntimeError('server_tts_unavailable')

    cleaned = clean_tts_text(text)
    if not cleaned:
        raise ValueError('text_required')

    voice = pick_server_tts_voice(language, gender)
    audio = asyncio.run(
        _synthesize_tts_audio(cleaned, voice, edge_rate_from_value(rate, language))
    )
    if not audio:
        raise RuntimeError('empty_audio')
    return audio, voice
