#!/bin/bash
# SaadAI Labs - Live Clipper: runs the job in output/job.json. Log: output/pipeline.log
cd "$(dirname "$0")/scripts" || exit 1
if command -v python3 >/dev/null 2>&1; then
  python3 run_pipeline.py "$@"
else
  echo "Python 3 is not installed. Install it from python.org, then try again."
  read -r -p "Press Return to close."
fi
