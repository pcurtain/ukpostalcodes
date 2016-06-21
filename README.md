**Hello Scurri Folks!!**

## In Progres...

Right now, there's a lot more discussion inline in the code than would probably
remain, but it's how I often work myself through lots of detailed
specifications.

The tests can be run via ```$python -m unittest test_postalcodevalidator```

The module itself can be imported as simply as:

```from ukpostalcodevalidator import validate```

and used with 

```result = validate(postalcode)```

## Code Choices

This solution is the one I thought would be most readable and worth discussion.
I also did some work on a purely regex version.  That would likely be how we'd
want a production version to be deployed, just because it's likely to be more
performant.  However! That version was much harder to review, validate and
debug.   Upside, it's maybe 8 lines and really fast.  Downside, it reads like
voodoo.  :)

Also, the current commit retains comments that we'd probaby clear out or trim.

## Production Next Steps

Before doing more with this, I'd want to dig into exact use cases.  If it's
part of a web service, we'd move most of it's behavior into the framework that
holds it and customize return values to suit, etc.  If it's callable from the
command line, we'd extend with getopts, etc.


