#!/bin/bash

pip install -r requirements.txt

sudo mkdir /opt/openai-search 
chmod +x main.py

printf "\nPlease enter your OpenAI API key:\n"
read api_key
sudo touch /opt/openai-search/.env
sudo chmod 666 /opt/openai-search/.env
echo $api_key > /opt/openai-search/.env

sudo cp main.py /opt/openai-search

echo 'alias ais="/opt/openai-search/main.py"' >> ~/.bashrc
if [ -f "/usr/bin/zsh" ]; then
 	echo 'alias ais="/opt/openai-search/main.py"' >> ~/.zshrc
fi

printf "\nInstallation finished successfully!\nThe program is installed to /opt/openai-search and we've added an alias to your bashrc (or zshrc)."
printf "\nBefore using the program please relogin or type:\n'source ~/.bashrc' - for bash; 'source ~/.zshrc' - for zsh"
/opt/openai-search/main.py
printf "\nSometimes it might take a while for OpenAI's servers to process your query, so don't panic if you don't get a response immediately :)\nEnjoy!\n"

rm -rf ../OpenAI-Search-main

