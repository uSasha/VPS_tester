FROM python:3.6.6-jessie

# avoid multiple threads from BLAS, since implicit already does threading for us
ENV OPENBLAS_NUM_THREADS 1

RUN mkdir -p /app/ \
    && chown -R nobody:nogroup /app

COPY requirements.txt /app/requirements.txt

RUN cd /app/ \
    && python -m venv /app/env \
    && /app/env/bin/pip install -r requirements.txt
ENV PATH /app/env/bin:$PATH

USER nobody
WORKDIR /app/
COPY cpu_test.py /app/
CMD ["python", "cpu_test.py"]
