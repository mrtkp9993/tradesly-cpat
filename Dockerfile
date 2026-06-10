FROM python:3.12-slim

WORKDIR /app

# Build and install the TA-Lib C library (required by the TA-Lib Python wheel).
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    g++ \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && curl -L -O https://github.com/TA-Lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz \
    && tar -zxf ta-lib-0.6.4-src.tar.gz \
    && cd ta-lib-0.6.4/ \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && cd .. \
    && rm -rf ta-lib-0.6.4 ta-lib-0.6.4-src.tar.gz

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]