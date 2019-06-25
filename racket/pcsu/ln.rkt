#lang racket/base

(require racket/cmdline)

(module+ test)

(module+ main
  (writeln (find-system-path 'run-file)) ;; name of the file that is executed
  (writeln (current-command-line-arguments))) ;; remainder of command line args
