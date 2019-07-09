#lang racket/base

(require racket/port)
(require racket/cmdline)
(require ffi/unsafe)

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

  ;; TODO: should we somehow signal a failing exit code when this is run? (i.e. non zero)
  (define (exn-handler exn file)
    (if (= (car (exn:fail:filesystem:errno-errno exn)) (lookup-errno 'ENOENT))
      (begin
        (display file (current-error-port))
        (displayln ": No such file or directory" (current-error-port)))
      (begin
        (display file (current-error-port))
        (displayln ": unspecified filesystem error occured" (current-error-port)))))

  (define port-list '())
  (for ((a arg-list))
    (with-handlers ((exn:fail:filesystem:errno? (lambda (exn) (exn-handler exn a))))
      (set! port-list (cons (open-input a) port-list))))
  (set! port-list (reverse port-list))
  ;; TODO: refactor to print out missing files at the point at which they
  ;; would be read into the output (like `cat` does). This may mean abandoning
  ;; the nice `input-port-append` proc we just started using :( .
  (define meta-input-port (apply input-port-append #f port-list))
  (copy-port meta-input-port (current-output-port))
  #|(for-each write-out-file arg-list)|#)
