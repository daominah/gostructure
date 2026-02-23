# `/cmd`

Executables go in the `/cmd` directory.
Usually, there is a main service along with some one-off scripts.

The directory name determines the default name of the binary output by `go build`.
Using a descriptive name instead of `main` is helpful,
for example when you need to find or kill the process.

It is common to have a small `main` func that only wires dependencies and starts the app,
importing and invoking code from the `/pkg` directory.

If an executable name contains multiple words, use hyphens to separate them.
This follows common CLI naming conventions.
But the source file names should still be in snake_case
to align with Go’s file naming conventions.

Examples:

* https://github.com/moby/moby/tree/master/cmd
* https://github.com/vmware-tanzu/velero/tree/main/cmd
* https://github.com/prometheus/prometheus/tree/main/cmd
* https://github.com/influxdata/influxdb/tree/master/cmd
* https://github.com/kubernetes/kubernetes/tree/master/cmd
* https://github.com/dapr/dapr/tree/master/cmd
* https://github.com/ethereum/go-ethereum/tree/master/cmd
