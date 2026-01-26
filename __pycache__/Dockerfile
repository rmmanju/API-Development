FROM python:3.9
WORKDIR /API DEVELOPMENT
COPY ./requirements.txt /API DEVELOPMENT/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /API DEVELOPMENT/requirements.txt
COPY ./app /API DEVELOPMENT/app
CMD ["fastapi", "run", "app/FHIRClientAPI.py", "--port", "80"]