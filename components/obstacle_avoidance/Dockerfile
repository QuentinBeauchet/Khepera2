FROM alpine:3.17.1

RUN apk add --no-cache python3

WORKDIR /app

COPY main.py .

ENTRYPOINT [ "python3" ]

CMD ["main.py"]