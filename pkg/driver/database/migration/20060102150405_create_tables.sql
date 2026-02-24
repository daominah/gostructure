-- +goose Up
-- +goose StatementBegin
CREATE TABLE products
(
    id         TEXT PRIMARY KEY,
    name       TEXT        NOT NULL DEFAULT '',
    price      INTEGER     NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE IF EXISTS products;
-- +goose StatementEnd
