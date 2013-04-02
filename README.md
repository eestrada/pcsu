#PCSU

**PCSU** stands for **P**OSIX **C**ompliant **S**hell **U**tilities; it is an effort to create a set of 100% POSIX compliant shell utilities as according to http://pubs.opengroup.org/onlinepubs/9699919799/. As far as I have been able to glean, there is no mention of implemention details for the utilities, only what their required behavior is. Thus, the initial effort is to create them in Py3K. Implentations in other languages, such as C99, may be added as during future efforts.

##Current Limitations

Certain utilities mention in the standard are currently beyond the scope of this project (and some may never be within the scope of this project).  A good example would be shell built-in commands (such as cd); these will not be implemented unless as POSIX compliant shell is also implemented for this project. A good example of a utility that is completely beyond the scope of this project would be creating a C compiler, so the c99 shell utility will likely never be implemented. Besides, there are number of mature and robust C compilers that are freely available (e.g. Clang, GCC, etc.).

##FAQ

####Other libraries of shell utilities already exist. Why create this project?

This project is mainly for my own learning and benefit. If it is useful to someone else, then all the better. Also, it would be nice to have a reference implementation of strictly POSIX compliant utilities. It also makes it possible for people testing shell scripts to be sure will be completely portable. Implementations such as the GNU coreutils often extend or sometimes even change the behavior of these core utilities; this can give a false impression of functionality that may not exist in all implementations. Having utilities that are strictly compliant allows portability testing that might not otherwise be possible.

####Why do the intial  implementation in Python 3.x?

Compared to other languages, Python is an easy language to use and fast to prototype in. Personal computers have become fast enough that slowdowns from an interpreted language will be relatively small, at least from a user's perception.

Although Python 3 is not yet as widespread as its predecessor, Python 2, it will never get to that point of saturation until more people start using it. Since this is a new project, I see no reason not to use the latest version of the language as the previous version is rapidly moving into EOL status. CUrrently, the utilities require at least version 3.2 since they utilitize the argparse module (the optparse module being deprecated since Python 2.7).

####Utility X isn't implemented and I really need/want it. Will you prioritize it?

I am currently only one person working on this in my free time, so my resources are limited. However, if you want a certain utility and have some skill in programing, you are free to contribute to the project. Your knowledge and support would be greatly appreciated.
