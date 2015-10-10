# ArpaEmrBot

Server side to handle a Telegram bot giving weather information provided from [Arpa Emilia-Romagna](http://www.arpa.emr.it/sedi.asp?idlivello=1504).

It's not an official bot, it's simply a reverse engineering/bridge to the Arpa webapp APIs. 

## Requirements

* weppy (5.0)

## Installation

The use of virtualenv is recommended:

    % git clone https://github.com/NonnEmilia/ArpaEmrBot
    % cd ArpaEmrBot
    % virtualenv env
    % . env/bin/activate
    % pip install -r requirements.txt
