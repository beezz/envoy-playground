
Modified frontend-proxy example from the official envoy repo used for testing
different connection failures cases, configurations of retries and circuit
breakers.

# Cases

- UC: Upstream connection termination in addition to 503 response code.

- UF: Upstream connection failure in addition to 503 response code.

- UO: Upstream overflow (circuit breaking) in addition to 503 response code.


- UC
```
curl 'localhost:9000/noretry?op=shutdown'
```

- UC,URX (With retries)
```
curl 'localhost:9000?op=shutdown'
```

- UC,UO

Connection termination with retries circuit breaking

```
siege -n 10 -c 10 'http://localhost:9000/?op=shutdown'
```

- UF,UO

Connection failure with retries circuit breaking

```
docker-compose stop service-{1,2,3}

siege -n 10 -c 10 'http://localhost:9000/?op=shutdown'
```

# Cascading failures & retries

Use the `frontend-envoy` -> `service-envoy` to test cascading failures.

# Notes

Use load testing tool that support (at least) HTTP 1.1. Otherwise configure
routes to accept also HTTP 1.0. ab does support only HTTP 1.0.
