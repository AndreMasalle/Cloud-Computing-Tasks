FROM --platform=linux/amd64 python:3.11

WORKDIR /app

RUN pip install --upgrade pip && pip install --no-cache-dir pyzmq rns

COPY . .

CMD ["bash"]