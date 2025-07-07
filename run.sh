#!/bin/zsh
cp .env.example .env
pip install pipenv
pipenv install

cd src || exit
python -m uvicorn main:app --reload
