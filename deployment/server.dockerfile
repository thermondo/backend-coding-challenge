ARG TAG=3.10-slim-bullseye
FROM python:${TAG}

ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# set timezone correctly
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN groupadd -g 1000 --system abanos; \
    useradd -u 1000 -g 1000 --system -m -s /sbin/nologin abanos

RUN apt-get update -qq > /dev/null \
    && apt-get install --no-install-recommends -y \
        make \
        gcc \
        g++ \
        tini > /dev/null


# System deps:
#RUN pip install "poetry"

RUN mkdir /srv/layer

WORKDIR /srv/layer

COPY --chown=abanos:abanos /backend/ /srv/layer/backend/

WORKDIR /srv/layer/backend

RUN pip3 install --upgrade pip==22.2.2 poetry

RUN cd /srv/layer/backend && POETRY_VIRTUALENVS_CREATE=false  poetry install --only main --no-root

RUN chown -R abanos:abanos /srv/layer/backend

USER abanos:abanos

EXPOSE 50050

CMD ["python","-m", "server"]



