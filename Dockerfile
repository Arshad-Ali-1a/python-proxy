FROM python:3.10
LABEL authors="Arshad Ali"

WORKDIR /app
COPY . .

EXPOSE 9001
CMD ["python", "-m", "pproxy.server", "-l", "http+socks4+socks5://:9001/"]
