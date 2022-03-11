# Build

## install requirements

```bash
pip install -r requirements.txt
```

## install mongodb on your localhost - [see how](https://docs.mongodb.com/manual/installation/)

for ubuntu
```bash
sudo apt-get install mongodb
```

## run the python app
```bash
python app/main.py
```
- type localhost:8000/docs in your browser

| :point_up:    | the defualt port for this app is 8000 |
|---------------|:------------------------|

## if you want to do it with uvicorn in shell delete this part from app/main.py
```python
if __name__ == '__main__' :
    uvicorn.run('main:app', debug=True)
```

## and then run this command in your shell

```bash
uvicorn app.main:app --reload
```

| :exclamation:   use (reload flag & debug=True) just for testing    |
|-----------------------------------------|
