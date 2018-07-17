# Find & Replace Processor

A simple find and replace processor for [Keboola Connection](https://connection.keboola.com/) written in [Python 3](https://www.python.org/).

It walks through .csv files within the /data/in/tables directory (and subdirectories) and replaces searched string with replacement line by line.

## Configuration parameters
**find**  The searched needle. *example: foo*
**replacement** The replacement text. *example: bar*
**encoding**  The input files encoding. *example: utf-8*
**debug** 0 for standard debug, 1 for hightened verbosity. *example: 0*

### Example configuration

Following configuration replaces all *foo*s with *bar*s.

```
{
  "find": "foo",
  "replacement": "bar",
  "encoding": "utf-8",
  "debug": 0
}
```
