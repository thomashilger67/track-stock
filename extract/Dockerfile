ARG TICKERS
FROM  python:3.13-alpine3.22

ENV TICKERS=${TICKERS}

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY main.py . 


CMD sh -c "python main.py ${TICKERS}"
