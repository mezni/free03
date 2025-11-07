# Multi-stage build
FROM rust:1.70-alpine as builder

RUN apk add --no-cache musl-dev openssl-dev openssl pkgconfig

WORKDIR /app

COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN cargo build --release

FROM alpine:3.18

RUN apk add --no-cache openssl ca-certificates && \
    update-ca-certificates

RUN addgroup -g 1000 -S app && \
    adduser -u 1000 -S app -G app

WORKDIR /app

COPY --from=builder /app/target/release/auth-service /app/auth-service
COPY config ./config

RUN chown -R app:app /app

USER app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["/app/auth-service"]
