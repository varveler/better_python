# Error Handling and Exceptions

> Code from https://github.com/ArjanCodes/betterpython/
> Text and ideas from: https://youtu.be/ZsvftkbbrR0

An error condition happens at run time that can be handled by the normal flow of execution of the code, is not a bug, because there is not a fix it can be done to avoid it, but rather some external factor  for example a file not found, a connection lost, etc. To properly manage error in code in python it has to be done with python Exceptions.

> Most programming languages make a distinction between syntax error during compiled or interpreter time and other error happening during run time. In **Python** that difference is less clear because parts of the program may be interpreted only when they are needed. Handling Errors it is done using Exceptions, both while interpreting and at run time.

Here we can find a simple code that does not handle error the proper way.
To start the server run:
```
  $python error-handling.py
```
In our browser we can go to url: localhost:5000/blogs and see we get all the data about the blogs. The problem begins when we try to fetch a specific blog that does not exists
>localhost:5000/blogs/some-not-existing-id

We get the following response:
```
Internal Server Error
```

The way to improve this is to implement Error Handling and Exceptions

Before Handling Exception Code:
```python
def fetch_blog(id: str):
    # connect to the database
    con = sqlite3.connect('application.db')
    cur = con.cursor()

    # execute the query and fetch the data
    # don't do this in production, prone to
    # SQL Injection attack!!!
    cur.execute(f"SELECT * FROM blogs where id='{id}'")

    #fetch the data and turn into a dictionary
    result = list(map(blog_lst_to_json, cur.fetchall()))

    # close the database
    con.close()
```

After Handling Exception Code:
```python
class NotFoundError(Exception):
    pass

class NotAuthorizedError(Exception):
    pass

def fetch_blog(id: str):
    try:
        # connect to the database
        con = sqlite3.connect('application.db')
        cur = con.cursor()

        # execute the query and fetch the data
        cur.execute(f"SELECT * FROM blogs where id=?", [id])
        result = cur.fetchone()

        # return the result or raise an error
        if result is None:
            raise NotFoundError(f'Unable to find blog with id {id}.')

        data = blog_lst_to_json(result)
        # check if it is public data else raise NotAuthorizedError
        if not data['public']:
            raise NotAuthorizedError(f'You are not allowed to access blog with id {id}.')
        return data
    except sqlite3.OperationalError as e:
        print(e)
        raise NotFoundError(f'Unable to find blog with id {id}.')
    # always close the connection to DB, finally block
    # executed whether and Error happened or not
    finally:
        print("Closing the database")
        # close the database
        con.close()
```
Also, exception can be handled on multiple levels. In the previous examples we handled error on the DB levels, to handle it on the view level we could do:
```python
from db import fetch_blogs, fetch_blog, NotFoundError, NotAuthorizedError


@app.route('/blogs/<id>')
def get_blog(id):
    try:
        return jsonify(fetch_blog(id))
    except NotFoundError:
        abort(404, description="Resource not found")
    except NotAuthorizedError:
        abort(403, description="Access denied")
```

## Context Managers

Python feature that allows to have a more fine control of what happens when objects are created or destroyed.

For example Python already has some useful context managers for opening a file, if you open a file and an Exception occurs, pythons makes sure that the file is closed if you used a "with" statment:

```python
#this will break
with open("not-existing-file.txt") as file:
    data = file.read()
    for line in data:
        print(line)
```
In order to do this for db query to SQLite you can create a context manager class that has 2 methods: enter and exit. "\_\_enter\_\_" method specifies what happens at creation time and "\_\_exit\_\_" what happens at destruction time.

```python
import sqlite3

class SQLite():
    def __init__(self, file='application.db'):
        self.file=file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        # return so we can use it latter
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        # this parameters: type, value, traceback won't
        # be used but they need to be there in order
        # to work correctly
        print("Closing the connection")
        self.conn.close()
```
Another advantage of using this class as a manager is that we have both creation and destruction in the same place which makes code more easy to organize.

Because we have this context manager we no longer need to use finally clause:

```python
def fetch_blog(id: str):
    try:
        # context manager "as" keyword assigns the
        # returned value to variable cur
        with SQLite('application.db') as cur:

            # execute the query and fetch the data
            cur.execute(f"SELECT * FROM blogs where id=?", [id])
            result = cur.fetchone()

            # return the result or raise an error
            if result is None:
                raise NotFoundError(f'Unable to find blog with id {id}.')

            data = blog_lst_to_json(result)
            if not data['public']:
                raise NotAuthorizedError(f'You are not allowed to access blog with id {id}.')
            return data
    except sqlite3.OperationalError:
        raise NotFoundError(f'Unable to find blog with id {id}.')
```

Exceptions are not perfect.
1. They introduce a Hidden Flow control in the program
2. If not careful may leak data in example: not closing a DB connection.
3. Exception may introduce extra coupling because high level system may need to know about low level exception objects.
