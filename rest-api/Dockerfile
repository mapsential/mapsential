FROM openjdk:17 as build

WORKDIR /workspace/app

COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY generate-application-properties.sh generate-application-properties.sh
COPY src src

ARG ENV

RUN ./generate-application-properties.sh ${ENV} && ./mvnw package -DskipTests

ENTRYPOINT java -jar target/mapsential-1.0.0.jar
