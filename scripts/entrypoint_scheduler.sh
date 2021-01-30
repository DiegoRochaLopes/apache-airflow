#!/usr/bin/env bash

echo "=== Installing python dependencies ==="
if [ -e "./scripts/requirements.txt" ]; then
    $(command -v pip) install --user -r ./scripts/requirements.txt
fi

airflow scheduler