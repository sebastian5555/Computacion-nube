FROM python:3.8
LABEL maintainer "Meinhard Ploner <dummy@host.com>"

WORKDIR /code

COPY kaggle.json /home/ubuntu/.kaggle/
COPY kaggle.json /root/.kaggle/
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY ./ ./

EXPOSE 80
CMD ["gunicorn", "--workers=1", "--log-level=debug","--timeout=60", "--bind=:80", "app:server"]
