# FROM python:3.9.4-alpine
# alpine base image does not work, even though the additional apk's and no error at image creation
FROM python:3.9.4
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
# RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev gmp-dev \
#  && pysmt-install --confirm-agreement --msat \
#  && apk del .build-deps
RUN pysmt-install --confirm-agreement --msat
CMD ["python", "app.py"]