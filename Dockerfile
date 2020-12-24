FROM ubuntu:21.04
# basic libs
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y wget build-essential gcc zlib1g-dev

# langage JP
RUN apt-get install -y locales \
    && locale-gen ja_JP.UTF-8 \
    && echo "export LANG=ja_JP.UTF-8" >> ~/.bashrc

# latest openssl for python
WORKDIR /root/
RUN wget https://www.openssl.org/source/openssl-1.1.1d.tar.gz \
        && tar zxf openssl-1.1.1d.tar.gz \
        && cd openssl-1.1.1d \
        && ./config \
        && make \
        && make install

# python
WORKDIR /root/
RUN wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz \
        && tar zxf Python-3.6.8.tgz \
        && cd Python-3.6.8 \
        && ./configure \
        && make altinstall
ENV PYTHONIOENCODING "utf-8"

WORKDIR /usr/local/bin/
RUN ln -s python3.6 python
RUN ln -s pip3.6 pip

# mecab
RUN apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8

ARG project_dir=/src/

ADD src/requirements.txt $project_dir

WORKDIR $project_dir

RUN pip install -r requirements.txt