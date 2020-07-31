FROM python:3.8-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

ARG PROJECT_ROOT
ARG MONITOR_USER
ARG MONITOR_GROUP
ARG UID
ARG GID
ARG DATA_PATH

RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

RUN pip install pip-tools
COPY requirements.in requirements.in
RUN pip-compile requirements.in && \
    pip install -r requirements.txt

RUN groupadd --gid $GID $MONITOR_GROUP && \
    useradd --uid $UID --home-dir /home/$MONITOR_USER --shell /bin/bash --gid $GID $MONITOR_USER

RUN chown -R $MONITOR_USER:$MONITOR_GROUP $PROJECT_ROOT

USER $MONITOR_USER
