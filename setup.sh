#!/bin/bash

pip install openai

printf "\nPlease enter your OpenAI API key:\n"
read api_key
sed -i "s/ENTER_YOUR_API/${api_key}/" ./main.py
chmod +x main.py

sudo mkdir /opt/openai-search 
sudo cp main.py /opt/openai-search

alias ais="/opt/openai-search/main.py"
#source ~/.bashrc 
if [ -f "/usr/bin/zsh" ]; then
 	alias ais="/opt/openai-search/main.py"
	#source ~/.zshrc 
fi

printf "\nThis will work for bash and zsh shells for curent user"
printf "\nIf you want to add this command for other users or your another shell add\n"
printf "\nalias ais='/opt/openai-search/main.py'\n"
printf "\nto .rc file of selected shell."
printf "\nAlso don't forget to type 'source ~/.bashrc' (or source ~/.zshrc) to apply changes.\n"
printf "\nSometimes it might take a while for OpenAI's servers to process "
printf "your query, so don't panic if you don't get a response immediately :)\n"

rm -r ../OpenAI-Search-main # What is it? :D
