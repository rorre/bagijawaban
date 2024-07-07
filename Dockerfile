FROM node:22-alpine AS tailwind_builder

WORKDIR /app

COPY package*.json /app/
RUN npm ci
COPY . /app/
RUN npx tailwindcss -i ./src/css/style.css -o ./static/css/style.css

FROM python:3.12-alpine AS runner

WORKDIR /app

COPY --from=tailwind_builder /app/static/css/style.css /app/static/css/style.css
COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-directory

COPY . .

ENTRYPOINT [ "python", "-m", "likulau.console", "run"]