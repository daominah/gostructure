package core

type Database interface {
	CreateFoo(v Foo) error
}

type Foo struct {
}
