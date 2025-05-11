FROM rabbitmq:3.7-management

COPY rabbitmq.conf /etc/rabbitmq
#COPY definitions.json /etc/rabbitmq

RUN cat /etc/rabbitmq/rabbitmq.conf