FROM golang:1.21.4-bookworm

COPY go.mod go.sum* /
RUN cd / && go mod download

ENV APP_DIR=/go/src/app
WORKDIR ${APP_DIR}
COPY . ${APP_DIR}
RUN cd ${APP_DIR}/cmd/main_example && go build

CMD ["/go/src/app/cmd/main_example/main_example"]
