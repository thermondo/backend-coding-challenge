ARG TAG=3.8-slim-bullseye
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

# Copy only requirements to cache them in docker layer
WORKDIR /code

COPY --chown=abanos:abanos /backend/ /code/backend/
COPY --chown=abanos:abanos /media/ /code/media/
# Creating folders, and files for a project:
COPY --chown=abanos:abanos poetry.lock pyproject.toml /code/

# Project initialization:
#RUN poetry config virtualenvs.create false \
#  && poetry install  --no-dev --no-interaction --no-ansi



#RUN sed -i 's/\r$//g' /code/backend/tasks_manager/celery_make.py
#RUN chmod +x /code/backend/tasks_manager/celery_make.py

RUN pip3 install --upgrade pip==22.2.2 poetry
RUN cd /code && POETRY_VIRTUALENVS_CREATE=false poetry install --no-dev

RUN chown -R abanos:abanos /code

USER abanos:abanos

RUN poetry install

CMD ["python", "-m", "backend.tasks_manager.celery_make"]