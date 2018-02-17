FROM registry.fedoraproject.org/fedora:27

LABEL maintainer = "Clement Verna <cverna@fedoraproject.org>"\
      summary = "libpagure development environment"\
      usage = "docker run -it --rm -v `pwd`:/code:z libpagure_dev"

RUN dnf -y install python2-requests python3-requests python2-flake8\
    python3-flake8 python2-pytest python3-pytest python3-pytest-cov\
    python2-pytest-cov python2-pytest-mock python3-pytest-mock

WORKDIR /code
ENV PYTHONPATH /code