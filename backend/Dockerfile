FROM python:3.10-slim

# Set timezone to IST
ENV TZ=Asia/Kolkata
RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get clean

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

