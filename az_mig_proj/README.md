# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following main points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
   

- Migrate a PostgreSQL database backup to an Azure Postgres database instance
   
- Refactor the notification logic to an Azure Function via a service bus queue message
   

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
   `az group create --location <closelocation> --name <appname>`
- Migrate and deploy the pre-existing web app to an Azure App Service

   `az webapp up --name techconfapp --location eastus --sku F1 --resource-group az_mig_proj`



2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder

---   
         Run the follwing to 
            - Create an Azure Database for PostgreSQL server on CLI or search Azure Postgres Database single server on portal
            - Configure server-level firewall rule
            - Get the connection information

         ``` bash
         az postgres server create --resource-group myresourcegroup --name <mydemoserver>  --location westus --admin-user <myadmin> --admin-password <server_admin_password> --sku-name B_Gen5_1

         az postgres server firewall-rule create --resource-group <myresourcegroup> --server <mydemoserver> --name all_IP --start-ip-address 0.0.0.0 --end-ip-address 255.255.255.255

         az postgres server show --resource-group <myresourcegroup> --name <mydemoserver>

         az postgres db create --name <techconfdb> --resource-group <myresourcegroup> --server-name <mydemoserver>
         ```
      - Migrate a PostgreSQL database backup to an Azure Postgres database instance
         `pg_dump -U postgres -W -F t -d bookreviewdb > C:\this\is\your\location\book_review.tar`

         `open pg admin> server_name > right-click on db_name > click restore Format: tar, Filename: open path to file > select OK`

3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan

5. Create a storage account

`az storage account create --name --resource-group`

---

6. Deploy the web app. (Make sure your are in the root of `web app` directory)
- Migrate and deploy the pre-existing web app to an Azure App Service

   `az webapp up --name techconfapp --location eastus --sku F1 --resource-group az_mig_proj`


### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.
   Use VS Code to create your service bus queue trigger and follow this -> [Link](https://github.com/Bayurzx/az_mig_proj/blob/master/function/ServiceBusQueueTrigger/__init__.py)

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
      follow this -> [Link](https://github.com/Bayurzx/az_mig_proj/blob/44b750a5f7af1d1f6c7693fb5cc722535c0d333e/web/app/routes.py#L86)
2. Re-deploy the web app to publish changes
   - You might need to delete the webapp with 
      `az webapp delete --name <mywebappname>`
   - Then recreate it here. Make sure you are in the root directory of the flask app `.../web` when deploying
      `az webapp up --name <mywebappname> --location <mylocation> --sku F1 --resource-group <resourcegroup>`

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* |   Basic  |    ~$26/month          |
| *Azure Service Bus*   |    Basic     |       $0.05/Million/Month       |
| ...                   |         |              |

## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.

- I used Consumption Plan for the Function App because
   -  Consumption plan charges you per `function request` and you get some milleage before getting charged

- I used App Service because
   -  App is very elastic and cost effective given that it could easily spin up to 10 VM instances during peak periods of operations and remove VM instances after peak periods at a cost of `$0.10/hour` in a Standard run production environment.