To build this project I have used the tech stack below
-PostgreSQL for data storage
-FastAPI for endpoint and request handling
-Celery for asynchronous task creation
-RabbitMq as a task queue

I approached the problem from data side as the app is mainly about data consumption and modification 
for this I have created a new database at my local postgres server

Created models for Continent, Country and City
The structure of these are pretty simple City instances has all the attributes like area, population, no_treees etc.
And the country and continent are basically key value pairs that are acting like containers of city and country.
By designing it this way we are free from redundancy as the only real information is stored at city level and country and continent level information is dynamically produced by querying the values and simply grouping by the desired entity.
This approach however has led to modification of the information only on city level meaning if you want to change a countries total population you should start by adding cities instead of directly modifying an integer value.
For data consistency it is better and if one wants to have country level data modification, we can always add same attributes to country level this will however duplicate the data and will require maintaining the database on every transaction like checking if any value inconsistency happened between transactions. I didn’t implement that as I think this method is way simpler and consistent on itself (plus I didn’t think that this task is about creating an all-round wiki page and more about designing a basic API)

Following on Model and db design I looked up a reasonable way of structuring a fastapi sql app and come up with 6 python files.

-models store the Orm models for the app.
-crud is the create read update delete operations implemented using orm and raw sql conventions I used both as I wanted to show I can access and manipulate data on different levels normally on production choosing one way is usually better but there is an ongoing debate about the helpfulness of Orm in general so I just used both methods mixed just for showing different approaches
-schemas are the pydantic model definitions my API requires the request body to have there is some typing and validation on the data so any broken request is automatically dropped by Fastapi itself without manual effort.
-database is a simple script that creates the db connections set and share session objects in a more separate cleaner way classes use.
-main is the main application where I run the FastAPi app that routes API endpoints and runs the app on uvicorn as a web app.
-celery_worker is the place where my celery tasks are defined, I just referenced required crud operations by importing them here this is where workers collect the celery operations and execute them.
-To run the application first I used a dockerized rabbitmq instance as it can cause compatibility issues running directly on shell on windows.
-This rabbitmq instance is running locally and using the default settings its ports are mapped to the local machine’s ports etc.
-Then I run the main file using python environment that I have created with the requirements defined in requirements.txt
-As a final step I opened another terminal window to create celery workers with the following command
celery -A celery_worker.celery worker -l info -P eventlet --pool=solo
PS: eventlet library is added as they have dropped windows support after version 4 and without it celery does not execute any task just collects them
In a real production environment, we can dockerize the entire application without the database with a virtual network and deploy it on an Azure or aws instance. I have also looked up about flower which lets users monitor the celery tasks that could be useful in a production environment.


