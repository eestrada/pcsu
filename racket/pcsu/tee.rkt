#lang racket/base

(require racket/cmdline)

(module+ test)

(module+ main
  (displayln (find-system-path 'run-file)) ;; name of the file that is executed
  (displayln (current-command-line-arguments))) ;; remainder of command line args
