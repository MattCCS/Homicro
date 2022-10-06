# Homicro
Home Microservices

A project to plan and organize home microservices.


## Concepts

### Self-Registration
- Services should be able to reach out to a central service to register themselves.
- Registration should be optional.
- The use of static port numbers should be minimized -- ideally only one.

### Freshness
- Health checks OR periodic checkins may be used to indicate service freshness or to discard entries.
- Competing services might try to overwrite each other's registrations.
    - Registrations could be kept by (NAME, IP, PORT) with overwrites disallowed until expiry time.
    - This would allow dead services to clear but duplicates not to push out live services.
- Services could declare that they never expire, in which case health checks could be required.

### Cross-Dependency
- Services should be able to discover each other through a central service.
- This should be optional, with start-time or run-time configuration as a fallback.
- How are services to be identified to minimize bootstrapping problems?
    - Central service should not have a list of names.
    - Services should self-declare names.
    - The central service should never have to be updated to support new services.


## Plan

### Self-Registration Endpoint
```
PUT /self-register
{
    "name": str,
    "expire": int,
}
```
- If NAME is not present, record is added.
    - Record is associated to (IP, PORT, EXPIRY).
    - Server can determine IP and PORT from socket.
    - If expire is 0, record does not expire.
- If NAME is present with no expiry, record is replaced.
- If NAME is present with expiry and IP and PORT match, record is refreshed with pre-recorded expiry.
- If NAME is present with expiry and IP and PORT don't match, request is ignoed.


### Discovery Endpoint
```
GET /discover
```
- Returns all services.
```
{
    str: {
        "ip": str,
        "port": int,
    },
}
```


### Discovery Endpoint (by name)
```
GET /discover/<name>
```
- Returns a specific service.
- Implies that names have to be URL-safe... not an obvious implication.
```
{
    "ip": str,
    "port": int,
}
```


### Health Checks
- Request is outbound to services that declared no expiry.
```
GET /health
```
- Returns name.
- If name mismatches to what's expected, record is discarded.


### Registration Endpoint
```
PUT /register
{
    "name": str,
    "expiry": int,
    "ip": str,
    "port": int,
}
```
- If request is not from localhost/loopback address, request is ignored.
    - Server can determine this from socket.
- ... (TBD)


