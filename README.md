# Ticketing

## About the project
this is a ticketing/supporting system that users can communicate with admins & explain their problems.
we decided to save repeated awnsers in which we call Templates. to organize Templates, we add another concept called Category.
each Template can be in just one Category.

Templatee structure:

    each Template has a title & description
    each Template is a subset of a Category

Category structure:

    each Category has a name
    each Category can be a subset of another Category

API end-points:

    create, edit and delete a Template
    list of all Templates in a Category
    create and edit a Category
    list of all Categories

## Prerequistiees
for running this project, you have to install the latest version of:

    python3, which you can download in https://www.python.org/downloads/
    pip: sudo apt install python3-pip
    pipenv: pip install pipenv
    add libraries: sudo apt install python3.10-venv

## How to run

now you have to clone the project into your machine.
cd to the project folder, create the virtual environment with the command "python3 -m venv .venv".

activate the environment:

    "soucre .venv/bin/activate" (Linux)
    ".venv\Scripts\activate" (Windows)

install all dependencies with commmand "pip install -r requirements.txt".

now you can start the web application on local-host port 5000 with "python app.py".

## Send request to the API endpoints

In order to send HTTP requests to API endpoints, use can use various methods like cURL, request libraries and so on.
in this case I want to use postman to do this. you can install postman from its website or plugin in vscode.

after running the app, you can send request with json objects for each API endpoint & see the result.

![postman request](https://github.com/pooyatfn/ticketing/assets/98226980/600fd359-a295-41ae-afea-520ffeb34b98)

