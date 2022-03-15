## Getting Started

- Start a virtual environment using venv.

- Then,install the requirements:

```bash
pip3 install -r requirements.txt
```

- Run the development server or (go to production instruction below):

```bash
flask run --host=localhost

Open [http://localhost:5000](http://localhost:5000) with your browser to see the result.

```


For production use gunicorn (or any other wsgi compatible server):

```bash
gunicorn -k gevent --bind 0.0.0.0:5000 --keep-alive 1 --workers 4 app:app
```


