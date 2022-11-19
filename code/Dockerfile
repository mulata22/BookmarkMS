FROM python
RUN pip install flask psycopg2; \
  rm -rf /code; \
  mkdir -p /code/bookman
COPY bookman /code/bookman
WORKDIR /code
CMD flask --app bookman run -h 0.0.0.0 