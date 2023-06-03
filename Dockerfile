FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

WORKDIR /app


RUN pip install Flask
RUN pip install requests
RUN pip install WSGIServer
RUN pip install gevent

COPY ./ ./

EXPOSE 8888

CMD ["python", "proxy_AG.py"]
