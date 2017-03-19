# PCSU

[![Run Status](https://api.shippable.com/projects/58afc19ab1c2a40600ebbf37/badge?branch=master)](https://app.shippable.com/github/eestrada/pcsu)

--------------------------------------------------------------------

**PCSU** stands for **P**OSIX **C**ompliant **S**hell **U**tilities;
it is an effort to create a set of 100% POSIX compliant shell
utilities according to the [POSIX.1-2008 standard]
(http://pubs.opengroup.org/onlinepubs/9699919799/). As far as I have
been able to glean, there is no mention of implemention details for
the utilities, only what their required behavior needs to be. Thus,
the initial effort is to create them in Py3K. Implentations in other
languages, such as Racket, may be added during future efforts.

Taking a page from the reference implementations of the PNG and
DEFLATE standards, **PCSU** is liberally licensed under the zlib
license. Thus, it can used almost anywhere for any purpose with the
one main caveat being the the license notice must accompany source
distributions. See the LICENSE file for details.

## Current Limitations

Certain utilities mention in the standard are currently beyond the
scope of this project (and some may never be within the scope of this
project).  A good example would be shell built-in commands (such as
cd); these will not be implemented unless/until a POSIX compliant
shell is also implemented as part this project. A good example of a
utility that is completely beyond the scope of this project would be
creating a C compiler, thus the c99 shell utility will likely never be
implemented as part of this effort. Besides, there are number of
mature and robust C compilers that are liberally licensed and freely
available (e.g. Clang, GCC, etc.).

## FAQ

#### Other libraries of shell utilities already exist. Why create this project?

This project is mainly for my own learning and benefit. If it is
useful to someone else, then all the better. Also, it would be nice to
have a reference implementation of strictly POSIX compliant
utilities. It also makes it possible for people testing shell scripts
to be sure their scripts will be completely portable. Implementations
such as the GNU Coreutils often extend or sometimes even change the
default behavior of these core utilities; this can give a false
impression of functionality that may not exist in all
implementations. Having utilities that are strictly compliant allows
portability testing that might not otherwise be possible.

#### Why do the intial implementation in Python 3.x?

Compared to most other languages, Python is easy to use and fast to
prototype in. Personal computers have become fast enough that
decreases in speed due to an interpreted language will be relatively
small, at least from a user's perception. Also, most bottlenecks in
programming are from IO, which is independent of implementation
language anyway.

Although Python 3 is not yet as widespread as its predecessor, Python
2, it will never get to that point of saturation until more people
start using it. Since this is a new project, I see no reason not to
use the latest version of the language since the previous version is
rapidly moving into EOL status. Currently, the utilities require at
least version 3.2 since they utilitize the argparse module (since
argparse is also included in Python 2.7, it may theoretically be
possible to use that version of Python as well, although no official
testing has been done to verify that).

Lastly, future implementations in other languages, such as Racket, are
both possible and probable.

#### Utility X isn't implemented yet and I really need/want it. Will you prioritize it?

I am currently only one person working on this in my free time, so my
resources are limited. However, if you want a certain utility and have
some skill in programing, you are free to contribute to the
project. Your knowledge and support would be greatly appreciated.
