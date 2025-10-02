#!/usr/bin/env bash
# Usage: source venv, then run this script
# Example:
#   source .venv/bin/activate
#   ./scripts/run_bot.sh

export PYTHONPATH=.
exec python -m bot.main
