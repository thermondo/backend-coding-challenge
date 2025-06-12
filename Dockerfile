FROM openjdk:25-jdk-slim

WORKDIR /app

COPY ./build/libs/*-SNAPSHOT.jar /app/app.jar

CMD ["java", "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005", "-jar", "/app/app.jar"]
EXPOSE 8081
