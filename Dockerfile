FROM owasp/zap2docker-stable

RUN pip3 install slackclient

COPY /app /app

ENTRYPOINT ["python3"]

CMD ["/app/owasp_zap_scan.py"]
