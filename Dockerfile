FROM python:3.9 as base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
USER root
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# builder is used to build dependencies (nautilus_trader)
FROM base as builder
WORKDIR $PYSETUP_PATH

# Install python dependencies
RUN python -m pip install --upgrade pip setuptools wheel poetry

# Install build deps
RUN apt-get update && apt-get install -y gcc

## We copy our Python requirements here to cache them and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN  poetry install --no-root
COPY . .
RUN poetry install

#FROM base as production
#COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
#WORKDIR $PYSETUP_PATH/nautilus_data

# Copy raw data
#COPY ./catalogs/EUDUSD202001 /catalog
#ENV CATALOG_PATH=/catalog
COPY ./scripts ./nautilus_data/scripts
RUN poetry run python -m scripts.hist_data_to_catalog

# Run backtest to generate data
RUN (cd nautilus_data && poetry run python -m scripts.example_backtest)
