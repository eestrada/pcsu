#lang info
(define collection "pcsu")
(define deps '("base"
               "rackunit-lib"))
(define build-deps '("scribble-lib" "racket-doc"))
(define scribblings '(("scribblings/pcsu.scrbl" ())))
(define pkg-desc "POSIX Compliant Shell Utilities, implemented in Racket.")
(define version "0.1")
(define pkg-authors '(eestrada))
