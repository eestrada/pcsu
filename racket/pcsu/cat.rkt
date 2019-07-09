#lang racket/base

(require racket/port)
(require racket/cmdline)

(module+ test)

(module+ main
  ;; name of the file that is executed
  ;;(writeln (find-system-path 'run-file))
  ;; remainder of command line args
  ;;(writeln (current-command-line-arguments))
  (define arg-list (vector->list (current-command-line-arguments)))
  (when (and (pair? arg-list)
             (equal? (car arg-list) "-u")) ;; No buffering is done anyway with copy-port, so this is pointless
    (set! arg-list (cdr arg-list)))
  (when (null? arg-list) ;; When it is just stdin -> stout
    (set! arg-list (list "-")))

  (define (open-input fstr)
    (if (equal? fstr "-")
      (current-input-port)
      (open-input-file fstr)))
  ;; TODO: add code to gracefully deal with non-existent files like `cat` does
  ;; (i.e. print an error to stderr and just skip the file)
  (define meta-input-port (apply input-port-append #f (map open-input arg-list)))
  (copy-port meta-input-port (current-output-port))
  #|(for-each write-out-file arg-list)|#)
