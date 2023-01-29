#!/bin/bash

if [ -e /opt/openai-search/main.py ]; then
    echo "OpenAI-Search is already installed!"
    printf "Do you want to remove the previous version? "
    read response
    if [[ $response == [Yy]es || $response == [Yy] ]]
    then
        printf "\nUninstalling the previous version...\n"
        sudo rm -rf /opt/openai-search
        sudo rm /usr/bin/ais
        sudo rm /usr/share/man/man1/ais.1.gz
        printf "The previous version uninstalled successfully!\nThe installation process will now continue as usual..."
    else
        printf "\nInstallation interrupted!\n"
        exit 0
fi

pip install -r requirements.txt

gzip docs/ais.1
sudo cp docs/ais.1.gz /usr/share/man/man1

sudo mkdir /opt/openai-search 

printf "\nPlease enter your OpenAI API key:\n"
read api_key
sudo touch /opt/openai-search/.env
sudo chmod 666 /opt/openai-search/.env
echo API_KEY=\'$api_key\' > /opt/openai-search/.env

chmod +x main.py
sudo cp src/main.py /opt/openai-search

sudo ln -s /opt/openai-search/main.py /usr/bin/ais
sudo chmod +x /usr/bin/ais

printf "\nInstallation finished successfully!\nThe program is installed to /opt/openai-search."
printf "\nTo view the manual, type: 'man ais'\n"
printf "\nSometimes it might take a while for OpenAI's servers to process your query, so don't panic if you don't get a response immediately :)\nEnjoy!\n"
