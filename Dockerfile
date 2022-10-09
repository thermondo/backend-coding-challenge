FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV HOMEDIR=/usr/src

WORKDIR $HOMEDIR

COPY poetry.lock pyproject.toml $HOMEDIR/
COPY . $HOMEDIR/.

RUN pip3 install poetry \
 && poetry install

COPY ./entrypoint.sh .
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]