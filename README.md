# Cave
This repo containes miscellanous utilities that can help:

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






