FROM python:3.12-alpine


RUN apk update && apk add --no-cache \
    git \
    curl \
    zsh \
    bash \
    starship \
    openssh \
    make \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers \
    openldap-clients \
    libaio \
    unzip \
    gcompat \
    && adduser -D -s /bin/zsh -u 1000 dev


USER dev

ENV PATH="/home/dev/.local/bin:${PATH}"
ENV ZSH_THEME starship
ENV HATSTALL_ENV=dev

COPY .zshrc /home/dev

SHELL ["/bin/zsh", "-c"]

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create true \
    && poetry config virtualenvs.prefer-active-python true \
    && poetry config virtualenvs.in-project true

WORKDIR /workspace
COPY ../ .


CMD ["tail", "-f", "/dev/null"]
