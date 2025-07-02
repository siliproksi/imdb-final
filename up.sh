#!/bin/bash
docker network create imdb 2>/dev/null || true
docker compose up --build
echo "Frontend: https://imdbfinal.codeise.com"
echo "Backend: https://imdbfinalb.codeise.com"