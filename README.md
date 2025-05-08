# VehicleDetector

The service uses the following technologies:


- `python ^3.13`
- `poetry ==2.1.3`
- `fastapi[standard] (>=0.115.12,<0.116.0)`
- `pillow (>=11.2.1,<12.0.0)`
- `ultralytics (>=8.3.129,<9.0.0)`


## How to run local environment via docker
```sh
$ git clone https://github.com/aeSYNK/...
$ docker-compose -f docker-compose.yml up --build -d
$ docker-compose logs # For see containers logs.
```

## How to run local environment via local machine

```sh
$ activate venv
$ pip install poetry
$ poetry install
$ cd app
$ fastapi dev main.py
```

## Docs URL:
http://127.0.0.1:8000/docs#/default/detect_vehicles_detect_vehicles__post


## How to decode images from response:
Go to https://base64.guru/converter/decode/image site
Paste there response like:
data:image/jpeg;base64,...