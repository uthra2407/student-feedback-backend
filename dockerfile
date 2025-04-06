# Use Python official image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Set the PIP timeout to 120 seconds
ENV PIP_DEFAULT_TIMEOUT=120


# Install dependencies
#RUN pip install --no-cache-dir --use-feature=fast-deps -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt -i https://pypi.org/simple

# Expose port 8000 (Django default)
EXPOSE 8000

# Run migrations and start Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]