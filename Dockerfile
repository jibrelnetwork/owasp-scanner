FROM owasp/zap2docker-stable
USER zap:zap

COPY /app /app

RUN pip3 install slackclient \
# && chown -R zap:zap /app \
 && chown -R zap:zap /zap

ENTRYPOINT ["python3"]

CMD ["/app/owasp_zap_scan.py"]
