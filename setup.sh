#!/bin/bash

pip install openai

printf "\nPlease enter your OpenAI API key:\n"
read api_key
sed -i "s/ENTER_YOUR_API/${api_key}/" ./main.py
chmod +x main.py

mkdir /opt/openai-search
mv main.py /opt/openai-search

printf "\nI don't know how to make a proper installer, so "
printf "you'll have add the following to your .bashrc file:"
printf "\nalias ais='/opt/openai-search/main.py'\n"

rm -r ../OpenAI-Search-main
