FROM python:3.9

ENV PYHTONUNBUFFERED=1
RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get -y install ffmpeg libsm6 libxext6

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860

ENTRYPOINT ["python", "ui.py"]