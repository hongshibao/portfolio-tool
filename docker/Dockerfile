ARG BASE_IMAGE
FROM ${BASE_IMAGE}

WORKDIR /app
COPY portfolio /app/portfolio
COPY resources/portfolio.csv /app/resources/
COPY Pipfile Pipfile.lock requirements.txt MANIFEST.in LICENSE README.md setup.py /app/
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "-m", "portfolio.app" ]
