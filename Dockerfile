FROM jupyter/minimal-notebook

ADD requirements.txt /usr/src/requirements.txt

USER root

RUN apt-get update && apt-get install -y libpq-dev \
  && pip install -r /usr/src/requirements.txt \
  && rm -rf /var/lib/apt/lists/* \
    /tmp/* \
    /var/tmp/* \
    /usr/share/man \
    /usr/share/doc \
    /usr/share/doc-base \
    ~/.cache/pip

RUN chmod -Rv 766 work

USER $NB_UID