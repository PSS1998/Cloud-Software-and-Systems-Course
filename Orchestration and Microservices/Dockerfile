FROM python:3.10.8-alpine3.16
WORKDIR /usr/app
RUN apk add build-base linux-headers zlib-dev jpeg-dev libjpeg-turbo
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]