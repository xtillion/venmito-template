FROM ubuntu:latest
LABEL authors="ltele"

ENTRYPOINT ["top", "-b"]