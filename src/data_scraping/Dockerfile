FROM python:3.11-slim-buster

WORKDIR /app

COPY . /app

ENV PYENV_SHELL=/bin/bash

RUN set -ex;  \   
    apt-get update && \
    apt-get upgrade -y && \   
    apt-get install -y --no-install-recommends build-essential git && \ 
    pip install --no-cache-dir --upgrade pip && \ 
    pip install pipenv requests bs4 python-docx Pillow && \
    pipenv --python python3 install --deploy --ignore-pipfile && \ 
    pipenv sync 


ENTRYPOINT ["/bin/bash"]

CMD ["-c", "pipenv shell"]
