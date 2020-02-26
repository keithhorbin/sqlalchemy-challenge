## Description

This project investigates a fictional trip to Hawaii in January 2020. It analyzes historical weather data for Hawaii collected at various weather stations to predict typical weather during the trip. This is done in the Jupyter notebook, while a Flask app is also created that allows data calls from a SQLite database using SQLAlchemy and Flask.

## Approach and File Structure

- SQLAlchemy in Python used to access SQL databases and allow data manipulation in Python using the Pandas package.
- In this case, SQLAlchemy is used to access the sqlite database (hawaii.sqlite) in the Resources folder. The two csv files hold the same data from the SQL database tables.
- The manipulation and visualization was done in a Jupyter Notebook.
- Data visualization images generated in the notebook are saved in the images folder.
- In app.py, the Flask library is used to simulate the generation of api calls from a SQL database. This application is run on the local host.

### Languages and Tools

- Python
- Pandas
- SQLAlchemy
- SQLite
- ORM Queries
- Flask
- Matplotlib
- JSON

### Files Included

* Jupyter Notebook of all analysis
* Python file containing a Flask API for Climate analysis
* Images folder containing output images
* Resources folder containing source data
