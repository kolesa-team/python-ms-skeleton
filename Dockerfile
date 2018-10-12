ARG base_image=python:3.6.6-jessie

FROM ${base_image}

ARG base_path=/var/www/app
ARG environment=Development
ARG version=not-set
ARG revision=not-set

ADD . ${base_path}

WORKDIR ${base_path}

RUN pip install -r requirements.txt && echo "python main.py --app web --env ${environment}" > run.sh

ENTRYPOINT /bin/bash run.sh

LABEL org.kolesa-team.image.maintainer="Dorofeev Fedor <dorofeev@kolesa.kz>" \
org.kolesa-team.image.name="ms-python" \
org.kolesa-team.image.version="${version}" \
org.kolesa-team.image.revision="${revision}" \
org.kolesa-team.image.base_image="${base_image}" \
org.kolesa-team.image.description="Python microservice template"