ARG PY_VERSION

FROM python:$PY_VERSION AS install

ARG PY_VERSION

ARG AIRFLOW_HOME
ENV AIRFLOW_HOME=$AIRFLOW_HOME

ARG AIRFLOW_VERSION
ENV AIRFLOW_VERSION=$AIRFLOW_VERSION

ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PY_VERSION}.txt"

RUN pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"


FROM install AS init

VOLUME ["${AIRFLOW_HOME}"]

EXPOSE 8080

RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY airflow/supervisord.conf /etc/supervisord.conf

ENTRYPOINT \
    airflow db init \
    && airflow users create -u "clemens" -e $(cat /run/secrets/email_clemens) -f "Clemens" -l "" -r "Admin" -p $(cat /run/secrets/airflow_password_clemens) \
    && airflow users create -u "denis" -e $(cat /run/secrets/email_denis) -f "Denis" -l "" -r "Admin" -p $(cat /run/secrets/airflow_password_denis) \
    && airflow users create -u "lucas" -e $(cat /run/secrets/email_lucas) -f "Lucas" -l "" -r "Admin" -p $(cat /run/secrets/airflow_password_lucas) \
    && airflow users create -u "orhun" -e $(cat /run/secrets/email_orhun) -f "Orhun" -l "" -r "Admin" -p $(cat /run/secrets/airflow_password_orhun) \
    && airflow users create -u "oscar" -e $(cat /run/secrets/email_oscar) -f "Oscar" -l "" -r "Admin" -p $(cat /run/secrets/airflow_password_oscar) \
    && /usr/bin/supervisord -c /etc/supervisord.conf
