FROM node:12.18.0 AS static_assets

WORKDIR /app

COPY package*json ./

RUN npm install

COPY . ./

RUN npm run build



FROM python:3.8.3

ENV PYTHONUNBUFFERED 1

RUN apt-get update                             && \
    apt-get install -y --no-install-recommends    \
        gdal-bin=2.4.0+dfsg-1+b1                  \
        gunicorn=19.9.0-1                      && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --no-input --clear

COPY --from=static_assets /app/maps /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cmdi.wsgi"]
