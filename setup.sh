#!/bin/bash

pip install openai

printf "\nPlease enter your OpenAI API key:\n"
read api_key
sed -i "s/ENTER_YOUR_API/${api_key}/" ./main.py
chmod +x main.py

sudo mkdir /opt/openai-search && mv main.py /opt/openai-search

echo "alias ais='/opt/openai-search/main.py" >> ~/.bashrc
source ~/.bashrc 
if [ -f "/usr/bin/zsh" ]; then
	echo "alias ais='/opt/openai-search/main.py" >> ~/.zshrc
	source ~/.zshrc 
fi

printf "\nThis will work for bash and zsh shells for curent user"
printf "\nIf you want to add this command for other users or your another shell add"
printf "\nalias ais='/opt/openai-search/main.py'\n"
printf "\n to .rc file of selected shell."
printf "Also don't forget to type 'source .bashrc' to apply changes.\n"
printf "\nSometimes it might take a while for OpenAI's servers to process "
printf "your query, so don't panic if you don't get a response immediately :)\n"

rm -r ../OpenAI-Search-main
