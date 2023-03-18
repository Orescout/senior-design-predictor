FROM python:3.8-buster

# Install poetry with pip
RUN pip install poetry

# Copy over
COPY poetry.lock ./
COPY pyproject.toml ./

# Install dependencies with poetry
RUN poetry install

# COpy over application code
COPY . .

# Add a CMD to start uvicorn appropriately
# CMD ["poetry", "run"]


# # Install Poetry
# # RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
# #     && poetry config virtualenvs.create false \
# #     && poetry install --no-dev

# # Copy the project files into the container
# COPY . /app
# WORKDIR /app

# RUN pip install --upgrade pip
# RUN pip install poetry
# RUN poetry config virtualenvs.create false
# RUN poetry install --no-dev

# # # Install the project's dependencies
# # RUN poetry install --no-dev

# # RUN pip install --upgrade pip
# # RUN pip install --no-cache-dir -r yolov5/requirements.txt
# # RUN pip install torch

# # Run the command
# CMD ["poetry", "run", "python", "main.py"]

