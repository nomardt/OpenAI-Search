#!/bin/bash

pip install openai

printf "\nPlease enter your OpenAI API key:\n"
read api_key
sed -i "s/ENTER_YOUR_API/${api_key}/" ./main.py
chmod +x main.py

sudo mkdir /opt/openai-search 
sudo cp main.py /opt/openai-search

echo 'alias ais="/opt/openai-search/main.py"' >> ~/.bashrc
alias ais="/opt/openai-search/main.py"
if [ -f "/usr/bin/zsh" ]; then
 	echo 'alias ais="/opt/openai-search/main.py"' >> ~/.zshrc
fi

printf "\nIf you want to add ais for other users/shell, add the following to *rc file:"
printf "\nalias ais='/opt/openai-search/main.py'\n"
printf "\nSometimes it might take a while for OpenAI's servers to process "
printf "your query, so don't panic if you don't get a response immediately :)\nEnjoy!\n"

rm -rf ../OpenAI-Search-main

