FROM python:3.8-slim

ARG STREAMLIT_PATH="/root/.streamlit/"

WORKDIR /src
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install streamlit
RUN pip install -r requirements.txt

RUN mkdir -p $STREAMLIT_PATH
COPY config.toml credentials.toml $STREAMLIT_PATH
COPY ./app /src/app

EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "app/__main__.py"]