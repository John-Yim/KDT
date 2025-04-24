#!/bin/bash

# 가상환경 활성화
source ~/miniconda3/bin/activate pytorch_env

# Flask 앱 위치로 이동
cd ~/Project_Note_complete

# 기존 gunicorn 종료 (이미 떠 있으면 종료)
pkill -f "gunicorn"

# gunicorn 백그라운드 실행
nohup gunicorn --bind 127.0.0.1:5000 'app:create_app()' > gunicorn.log 2>&1 &

# 기존 cloudflared 종료 (이미 떠 있으면 종료)
pkill -f "cloudflared tunnel"

# cloudflared 백그라운드 실행
nohup cloudflared tunnel run my-project-tunnel > cloudflared.log 2>&1 &
