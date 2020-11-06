FROM python:3
RUN mkdir /code
RUN pip --no-cache-dir install \
    flask \
    pyyaml \
    uwsgi
COPY ./app /code
ADD https://github.com/bilibili/flv.js/releases/download/v1.5.0/flv.min.js /code/static/flv.min.js
RUN chmod 644 /code/static/flv.min.js
USER nobody
WORKDIR /code
