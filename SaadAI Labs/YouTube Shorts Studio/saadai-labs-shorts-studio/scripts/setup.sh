#!/usr/bin/env bash
# One-time setup for Shorts Studio. Works on macOS (Claude Code) and Linux (claude.ai code sandbox).
# Safe to re-run: skips what is already there and refreshes the engine source from the skill.
set -e
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
HOME_DIR="${SHORTS_STUDIO_HOME:-$HOME/.shorts-studio}"
ENGINE="$HOME_DIR/engine"
OS="$(uname -s)"
mkdir -p "$HOME_DIR/models" "$ENGINE"
export PIP_NO_INPUT=1 PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring

pipi() { python3 -m pip install -q "$@" 2>/dev/null || python3 -m pip install -q --user "$@" 2>/dev/null || python3 -m pip install -q --break-system-packages "$@"; }

command -v node >/dev/null || { echo "ERROR: Node.js 18+ is required (macOS: brew install node)"; exit 1; }
if ! command -v ffmpeg >/dev/null; then
  if [ "$OS" = Darwin ]; then brew install ffmpeg
  elif command -v apt-get >/dev/null; then (apt-get update -qq && apt-get install -y -qq ffmpeg) || sudo apt-get install -y -qq ffmpeg
  fi
fi
command -v ffmpeg >/dev/null || { echo "ERROR: ffmpeg is required and could not be installed"; exit 1; }
if ! command -v whisper-cli >/dev/null && [ "$OS" = Darwin ] && command -v brew >/dev/null; then
  echo "installing whisper.cpp (exact word timing for captions)..."; brew install whisper-cpp || true
fi
# Linux has no Apple emoji font: install Noto Color Emoji so emoji illustrations render
if [ "$OS" = Linux ] && ! fc-list 2>/dev/null | grep -qi "color emoji"; then
  (apt-get install -y -qq fonts-noto-color-emoji fontconfig || sudo apt-get install -y -qq fonts-noto-color-emoji fontconfig) >/dev/null 2>&1 || echo "note: could not install an emoji font; emojis may not render"
fi
command -v whisper-cli >/dev/null || echo "note: whisper-cli not found; captions will use estimated word timing"
python3 -c "import numpy, PIL" 2>/dev/null || pipi numpy pillow

# engine source -> ~/.shorts-studio/engine (node_modules and generated voice/music are kept)
mkdir -p "$ENGINE/public/p" "$ENGINE/public/music"
(cd "$SKILL/engine" && tar cf - --exclude node_modules --exclude 'public/p' --exclude 'public/music' .) | (cd "$ENGINE" && tar xf -)
if [ ! -d "$ENGINE/node_modules/remotion" ]; then
  echo "installing the Remotion engine (one time, ~1-2 min)..."
  (cd "$ENGINE" && npm install --no-audit --no-fund --loglevel=error)
fi
(cd "$ENGINE" && npx remotion browser ensure >/dev/null 2>&1) || echo "note: Remotion could not pre-download its headless browser; rendering will try again (needs internet)"

# Whisper model for word timestamps (~148 MB), only if whisper-cli exists and no model is present
if command -v whisper-cli >/dev/null; then
  if ! ls "$HOME_DIR"/models/ggml-*.bin >/dev/null 2>&1 && [ ! -s "$HOME/.saadai-reel-editor/models/ggml-large-v3-turbo-q5_0.bin" ]; then
    echo "downloading Whisper base.en model (~148 MB)..."
    curl -sSL -o "$HOME_DIR/models/ggml-base.en.bin" "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"
  fi
fi

# Kokoro: free, local, realistic neural voices (default narrator: a male US voice blend)
[ -x "$HOME_DIR/venv/bin/python" ] || python3 -m venv "$HOME_DIR/venv"
"$HOME_DIR/venv/bin/python" -c "import kokoro_onnx, soundfile" 2>/dev/null || {
  echo "installing the Kokoro voice engine..."
  "$HOME_DIR/venv/bin/pip" install -q --no-input --progress-bar off kokoro-onnx soundfile
}
mkdir -p "$HOME_DIR/models/kokoro"
KREL="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
[ -s "$HOME_DIR/models/kokoro/kokoro-v1.0.onnx" ] || { echo "downloading Kokoro voice model (~310 MB)..."; curl -fsSL -o "$HOME_DIR/models/kokoro/kokoro-v1.0.onnx" "$KREL/kokoro-v1.0.onnx"; }
[ -s "$HOME_DIR/models/kokoro/voices-v1.0.bin" ] || curl -fsSL -o "$HOME_DIR/models/kokoro/voices-v1.0.bin" "$KREL/voices-v1.0.bin"

[ -s "$ENGINE/public/music/upbeat.wav" ] || python3 "$SKILL/scripts/music.py"
echo "Shorts Studio ready: engine at $ENGINE"
