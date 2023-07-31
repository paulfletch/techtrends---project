#Base Image
FROM python:3.8.17-alpine3.18  

# Working directory
WORKDIR /app

# Copy files 
COPY ./techtrends .

# update pip 
RUN pip install --upgrade pip

# Install specified packages
RUN pip install -r requirements.txt

# Ensure Database is initialised 
RUN python init_db.py

#Expose application port
EXPOSE 3111

# Start application
CMD [ "python", "app.py" ]

# Run built-in healthcheck on app using status page.  This checks the health of the app and underlying database


#Use a Python base image in version 3.8
#Expose the application port 3111
#Install packages defined in the requirements.txt file
#Ensure that the database is initialized with the pre-defined posts in the init_db.py file
#The application should execute at the container start