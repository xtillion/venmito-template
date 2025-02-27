FROM openjdk:17-jdk-alpine
MAINTAINER baeldung.com
ENV DATABASE_URL=jdbc:mysql://some-mysql:3306/mydatabase
ENV DATABASE_USER=root
ENV DATABASE_PASSWORD=my-secret-pw
ENV SERVER_USER=admin
ENV SERVER_PASSWORD=password
COPY /build/libs/profileService-0.0.1-SNAPSHOT.jar profileService-0.0.1-SNAPSHOT.jar
ENTRYPOINT ["java","-jar","/profileService-0.0.1-SNAPSHOT.jar"]