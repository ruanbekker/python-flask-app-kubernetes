FROM maven:3.6.3-openjdk-15 as builder
WORKDIR /app
COPY . /app
# use buildit for caching
# docker builder prune --filter type=exec.cachemount to delete cache
RUN --mount=type=cache,target=/root/.m2 mvn -f /app/pom.xml clean package

FROM adoptopenjdk:15-jre-hotspot
ARG JAR_FILE=/app/target/*.jar
WORKDIR /app
COPY --from=builder $JAR_FILE /app/app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-XshowSettings:vm", "-XX:NativeMemoryTracking=summary", "-jar", "/app/app.jar"]
