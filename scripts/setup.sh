#!/usr/bin/env bash
# Installiert HyperFrames-CLI, GSAP, Chrome Headless Shell und die Piper-Stimmen.
set -euo pipefail
cd "$(dirname "$0")/.."
npm install --no-audit --no-fund
npx hyperframes browser ensure
pip install -q piper-tts scipy numpy librosa 2>/dev/null || pip install -q --break-system-packages piper-tts scipy numpy librosa
mkdir -p /root/tts
for v in thorsten karlsson pavoque; do
  [ -f "/root/tts/de-$v-low.onnx" ] && continue
  curl -sSL "https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-$v-low.tar.gz" | tar xz -C /root/tts
done
# Werkzeuge (Nutzer 23.11.): ffmpeg, yt-dlp, Whisper (Sprache -> Text). Die Stimme bleibt ElevenLabs.
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
command -v yt-dlp >/dev/null || pip install -q --no-cache-dir yt-dlp 2>/dev/null || pip install -q --no-cache-dir --break-system-packages yt-dlp
command -v whisper >/dev/null || pip install -q --no-cache-dir openai-whisper 2>/dev/null || pip install -q --no-cache-dir --break-system-packages openai-whisper
