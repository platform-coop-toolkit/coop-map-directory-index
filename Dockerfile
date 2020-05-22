FROM node:12 AS static_assets

WORKDIR /app

COPY package*json ./

RUN npm install

COPY . ./

RUN npm run build



FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update                                                      && \
    apt-get install -y --no-install-recommends gdal-bin=2.4.0+dfsg-1+b1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app/

COPY --from=static_assets /app/maps /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
