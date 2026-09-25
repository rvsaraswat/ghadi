# Stage 1: Build the Flutter Web application
FROM debian:stable-slim AS build-env

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git unzip xz-utils zip libglu1-mesa \
	&& rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch stable https://github.com/flutter/flutter.git /usr/local/flutter
ENV PATH="/usr/local/flutter/bin:/usr/local/flutter/bin/cache/dart-sdk/bin:${PATH}"

ARG API_BASE_URL=http://localhost:28000

RUN flutter doctor
RUN flutter config --enable-web

WORKDIR /app
COPY . .
RUN flutter create . --platforms web
RUN flutter pub get
RUN flutter build web --release --dart-define=API_BASE_URL=${API_BASE_URL}

# Stage 2: Serve the built web files using Nginx
FROM nginx:alpine
COPY --from=build-env /app/build/web /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
