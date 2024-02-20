### Make certificate (do not turn off nginx http only)

```bash
openssl req -newkey rsa:2048 -sha256 -nodes -keyout YOURPRIVATE.key -x509 -days 365 -out YOURPUBLIC.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=YOURDOMAIN.EXAMPLE"
```
### Start ngrok
```bash
ngrok http http://localhost:8080 --domain=yourdomainhere
```

# Run 
```bash
docker compose up --build
```
