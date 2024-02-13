#!/bin/bash

# source .venv/bin/activate && \
pip install -r requirements.txt && \
pip install -U pytest && \
pip install ruff && \
pip install pre-commit && pre-commit install