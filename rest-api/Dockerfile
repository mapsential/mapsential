FROM openjdk:16-ea-1 as build

WORKDIR /workspace/app

COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY src src

RUN mkdir -p /etc/config/datasource && \
    ln -s /run/secrets/postgres_password /etc/config/datasource/password

RUN ./mvnw package -Dprofile=prod -DskipTests


FROM build AS run

EXPOSE 8080

ENTRYPOINT java -jar target/mapsential-0.0.1-SNAPSHOT.jar