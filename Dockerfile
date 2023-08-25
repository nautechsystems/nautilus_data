FROM python:3.10-slim as base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup"
ENV PATH="/root/.cargo/bin:$POETRY_HOME/bin:$PATH"
WORKDIR $PYSETUP_PATH

FROM base as builder

# Install build deps
RUN apt-get update && apt-get install -y clang curl

# Install Rust stable
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install project
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main
COPY . ./
RUN poetry install

FROM base as application

ENV CATALOG_PATH=/catalog

# Copy python environment from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY ./scripts $PYSETUP_PATH/scripts

# Generate data catalog
RUN python -m scripts.hist_data_to_catalog

# Run backtest to generate data
#RUN python -m scripts.example_backtest
