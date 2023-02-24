FROM docker.io/python:3.11.2-alpine

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="Unstack Folders" \
      org.opencontainers.image.description="Copy deeply nested files to the base level"

WORKDIR /usr/local/src/pl-unstack-folders

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["unstack", "--help"]
