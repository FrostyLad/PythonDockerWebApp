FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV STATIC_INDEX 1
COPY ./webapp /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python main.py runserver 0.0.0.0:8000
