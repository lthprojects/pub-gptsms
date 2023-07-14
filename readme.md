# ChatGPT SMS

## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Variables](#variables)
* [Setup](#setup)

## General info
This project uses an API endpoint in Azure App Service and Azure Communication Service to make OpenAI's API functions available via SMS. The API was developed using Python/Flask and currently runs in a free tier Web App instance. 
The Python API:
1. Accepts incoming Azure Communication Service SMS messages via event grid 
2. Processes the data 
3. Sends the data.message key value to the ChatGPT API
4. Returns GPT's response via SMS 
	
## Technologies
Project is created with:
* Python (see requirements.txt)
* Azure App Service
* Azure Communication Service
* OpenAI ChatGPT API

## Variables
Sensitive variables are set via the Web App application settings. 
* GPT_KEY: ChatGPT developer API key
* COM_ENDPOINT: Communication Service connection string 
* SMS_NUMBER: Public phone number linked to Communication Service

## Setup