FROM ubuntu:18.04

ARG PYTHON_VERSION

WORKDIR /application

COPY sample_python .

ADD https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz .
ADD https://bootstrap.pypa.io/get-pip.py .

RUN apt update
RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
    apt-get install python3.8 -y; \
  else \
    apt -y install wget build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev uuid-dev; \
  fi
RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
    apt install python3.8-distutils -y; \
  else \
    tar -xf Python-3.9.0.tgz; \
  fi
RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
    apt-get -y install wget; \
  else \
    ./Python-3.9.0/configure; \
  fi
RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
    python3.8 get-pip.py; \
  else \
    make altinstall; \
  fi
RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1; \
  else \
    python3.9 get-pip.py; \  
  fi
RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
    python3.8 -m pip install pytest; \
  else \
    python3.9 -m pip install pytest; \
  fi
RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
    python3.8 -m pip install nbmake; \
  else \
    python3.9 -m pip install nbmake; \
  fi
RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
    python3.8 -m pip install pylint; \
  else \
    python3.9 -m pip install pylint; \
  fi

