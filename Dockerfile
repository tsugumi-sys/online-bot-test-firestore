FROM python:3.9-slim

WORKDIR /src

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

COPY ./app /src/app
COPY ./secrets /src/secrets
COPY ./scripts/entrypoint.sh /src/scripts/

RUN chmod +x /src/scripts/entrypoint.sh
CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080" ]