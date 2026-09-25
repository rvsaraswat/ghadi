# Stage 1: Build the Flutter Web application
FROM debian:stable-slim AS build-env

RUN apt-get update && apt-get install -y curl git unzip xz-utils zip libglu1-mesa

RUN git clone https://github.com/rvsaraswat/ghadi
ENV PATH="/usr/local/flutter/bin:/usr/local/flutter/bin/cache/dart-sdk/bin:${PATH}"

RUN flutter doctor
RUN flutter config --enable-web

WORKDIR /app
COPY . .
RUN flutter pub get
RUN flutter build web --release

# Stage 2: Serve the built web files using Nginx
FROM nginx:alpine
COPY --from=build-env /app/build/web /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
