FROM python
RUN mkdir -p /home/src
COPY . /home/src
WORKDIR /home/src
RUN pip install -r /home/src/requirements.txt