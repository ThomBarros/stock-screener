# Stock Screener App

j

## Installation

Clone the repository, then create a virtual environment in the base directory:
```
cd stock-screener
python -m venv venv
venv/Scripts/activate
```
where `venv` is the name of the virtual environment.

Install required packages using:
```
pip install -r requirements.txt
```
Install Nodejs and add to the System variables Path. Then install frontend packages with:
```
cd frontend
npm install
```

To start the backend:
```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
And to start the frontend run:
```
cd frontend
npm start
```

The web app should appear on `http://localhost:3000/`