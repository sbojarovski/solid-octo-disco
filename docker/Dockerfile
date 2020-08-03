FROM python:3.8-slim

RUN apt-get update && apt-get install -y libpq-dev gcc postgresql-client

ARG PROJECT_ROOT
ARG MONITOR_USER
ARG MONITOR_GROUP
ARG UID
ARG GID
ARG DATA_PATH

RUN groupadd --gid $GID $MONITOR_GROUP && \
    useradd --uid $UID --home-dir /home/$MONITOR_USER --shell /bin/bash --gid $GID $MONITOR_USER

RUN mkdir -p /entrypoint.d
COPY ./docker/wait_for_postgres.sh /entrypoint.d/
COPY ./docker/wait_for_kafka.py /entrypoint.d/

RUN mkdir -p /cert
ADD ./docker/cert /cert/

RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

RUN pip install pip-tools
COPY requirements.in requirements.in
RUN pip-compile requirements.in && \
    pip install -r requirements.txt

RUN chown -R $MONITOR_USER:$MONITOR_GROUP $PROJECT_ROOT
RUN chown -R $MONITOR_USER:$MONITOR_GROUP /entrypoint.d/
RUN chown -R $MONITOR_USER:$MONITOR_GROUP /cert/
RUN chmod u+x /entrypoint.d/wait_for_postgres.sh

USER $MONITOR_USER
