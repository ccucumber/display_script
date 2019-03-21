FROM python
COPY . /usr/src/mpp
WORKDIR /usr/src/mpp
RUN pip install -r requirements.txt
EXPOSE 84
EXPOSE 8086

CMD ["python", "main.py"]
