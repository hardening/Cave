# Cave
This repo contains miscellanous utilities that can help:

* malloc-check.py: this script tries to find unchecked calls to malloc / calloc / strdup / _strdup. The script is very basic, it works well when you have a sane codestyle.

It considers that this case is checked by the caller
```C
void *my_func() {
  /* code here */
    return malloc(12);
}

```
It will check for 
```C
a = b = malloc(12);
```
and will try to find a if statement in the 5 next lines checking for either a or b.

If we have this
```C
if ((a = malloc(12))) {
  /* code */
}
```
it considers it as a checked malloc call.

The script can be invoked with:

* no argument: it will do a *git ls-files* and will do checks on these files;
* *--stdin*: it will scan files taken from stdin with with one filename per line;
* a filename: it will read the file and consider it contains the list of files to scan (one filename per line)

Checks are done in file with the c, cpp and cxx extension.




