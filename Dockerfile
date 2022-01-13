FROM ubuntu:18.04
RUN apt-get update

RUN apt-get install -qy git wget
RUN GO_VERSION=go1.16.10.linux-amd64.tar.gz &&\
    cd /opt &&\
    wget --quiet https://dl.google.com/go/$GO_VERSION &&\
    tar -C /usr/local -xzf $GO_VERSION &&\
    rm /opt/$GO_VERSION

RUN mkdir -p /go/src
ENV GOPATH=/go
ENV GOROOT=/usr/local/go
ENV PATH="$PATH:$GOROOT/bin:$GOPATH/bin"

RUN apt-get install -qy graphviz gcc

RUN TMP='package main; func main() {println("Hello world")}' &&\
    mkdir -p /go/src/hello &&\
    echo $TMP> /go/src/hello/hello.go

RUN apt-get install -qy procps net-tools telnet iputils-ping vim gettext-base

COPY go.mod /go.mod
COPY go.sum /go.sum
RUN cd / && go mod download

ENV APP_DIR=/go/src/app
WORKDIR ${APP_DIR}
COPY . ${APP_DIR}
RUN cd ${APP_DIR}/cmd/example && go build

CMD ["bash", "-c", "${APP_DIR}/cmd/example/example"]
