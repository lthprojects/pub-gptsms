# ChatGPT SMS

# Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Variables](#variables)
* [High Level Setup](#high-level-setup)

# General info
This project uses an API endpoint in Azure App Service and Azure Communication Service to make OpenAI's API functions available via SMS. The API was developed using Python/Flask and currently runs in a free tier Web App instance. 
The Python API:
1. Accepts incoming Azure Communication Service SMS messages via event grid 
2. Processes the data 
3. Sends the data.message key value to the ChatGPT API
4. Returns GPT's response via SMS 
	
# Technologies
Project is created with:
* Python (see requirements.txt)
* Azure App Service
* Azure Communication Service
* OpenAI ChatGPT API

# Variables
Sensitive variables are set via the Web App's application settings. 
* GPT_KEY: ChatGPT developer API key
* COM_ENDPOINT: Communication Service connection string 
* SMS_NUMBER: Public phone number linked to Communication Service
* AUTH_NUMBER: Private cell number used to validate running custom functions 

# High Level Setup
Start by forking this project. 

## OpenAI API 
Docs: https://platform.openai.com/overview
1. Mosey on over to OpenAI and create yourself a developer account. 
2. Setup billing and create yourself an API key. This is your "GPT_KEY". 

## Create Azure App Service 
Docs: https://learn.microsoft.com/en-us/azure/app-service/
1. Create an App Service Plan. The free tier works just fine. 
2. Create a new Web App.
3. Under "Networking", click on "Access Restrictions". 
4. Under "Site access and rules", add an allow rule for "Service Tag" "AzureEventGrid". 
    * Bonus points if you setup your own auth flow vs relying on network accees rules. 
5. Add another allow rule for "IPv4" and add your public ip. 
6. Make sure "Unmatched rule action" is set to deny to minimize unnecessary traffic. 

## Setup Azure Communication Service 
Docs: https://learn.microsoft.com/en-us/azure/communication-services/
1. Head over to Azure and create an Azure Communication Service instance. 
2. Delegate a phone number. This is your "SMS_NUMBER".
3. Go to keys and copy one of the "Connection string" keys. Either one will work. This is the value for your "COM_ENDPOINT" variable. 

## Setup Azure App Service 
Now for the fun part. Let's finish setting up the Azure Web App. 
1. Head back over to your Web App and go to the "Configuration" tab. 
2. Under "Application settings", reference the "Variables" section above and input the respected variables and their values from previous steps. 
3. Next, go to the "Deployment Center". 
4. You can use a number of different deployment methods here, but the easist will be the Github integration. 
5. Setup the Github integration and deploy. Give it a couple minutes to complete the deployment.

## Setup Event Grid 
We need to setup event grid to send incoming sms messages to our API endpoint. 
1. Go to events in your Azure Communication Service instance. 
2. Click Event Subscription. 
3. Fill out with the below info and click create. 

### Create Event Subscription: 
* Name: Whatever you want
* Event Schema: Cloud Event Schema 
* Filter to Event Types: SMS Received
* Endpoint Type: Web Hook 
* Endpoint: Your App Service URL plus /incoming-sms. ie "https://example.azurewebsites.net/incoming-sms"
* Bonus points if you use the advanced filters to lock it down to only numbers you choose. 

## Test
* If everything worked correctly... you should be able to navigate to "https://example.azurewebsites.net/test" and get a success message. 
* Try sending an SMS message to your provisioned number. 
* If something isn't working you can start by looking at the web app "Log stream". 
* Enjoy! 