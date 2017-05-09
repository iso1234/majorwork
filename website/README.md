# majorwork
My year 12 software design and development major work

### How to run the server
    > Open a terminal window in /majorwork
    > Run the following command command (without the '$')
    $ python3.6 app.py
    > Go to 'http://localhost:5000' in your internet browser.


### Dependencies
* Flask (0.12)
* Python (3.6.0)
* Sqlite (3.8.10.2)


### How to create database:        
    1. Open a python3 shell in /majorwork
    2. Input the following commands in the python3 shell (without the '>>>')
    >>> import configDB
    >>> configDB.createDB()
    3. Thats it! You can now run the server and it will connect to the database.
  Note: If a file called 'main.db' already exists you must delete it to create a new one; these commands don't overwrite a pre-existing file and therefore will not create a new database if 'main.db' exists.
