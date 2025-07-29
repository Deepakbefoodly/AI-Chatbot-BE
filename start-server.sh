#!/usr/bin/env bash

set
exec uvicorn --reload --proxy-headers  --host 0.0.0.0 --port 8000 src.main:app