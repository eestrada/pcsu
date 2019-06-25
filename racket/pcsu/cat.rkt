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
  (when (equal? (car arg-list) "-u") ;; No buffering is done anyway with copy-port, so this is pointless
    (set! arg-list (cdr arg-list)))
  (define (copy-io)
    (copy-port (current-input-port) (current-output-port)))
  (define (write-out-file fp)
	(if (equal? fp "-")
	  (copy-io)
	  (with-input-from-file fp copy-io)))
  ;; TODO: add code for case of no CLI arguments (i.e. just pipe stdin to stdout)
  (for-each write-out-file arg-list))
