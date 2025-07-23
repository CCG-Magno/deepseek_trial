FROM python:3.13

#RUN adduser -D nonroot &&\
RUN   mkdir /home/app/ 
#&& chown -R nonroot:nonroot /home/app
WORKDIR /home/app
#USER nonroot
ENV DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY
#COPY --chown=nonroot:nonroot . .
COPY . .

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

CMD ["python", "test.py"]
