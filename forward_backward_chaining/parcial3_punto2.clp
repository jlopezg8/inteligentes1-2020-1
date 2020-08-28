(deffacts the-facts
    (lte 0 3)
    (lte 7 9))


; There's no fact of type "number", and no rule produces a fact of this type,
; so this rule is useless:
(defrule c
    ; Cannot bind a variable to a single-field fact (i.e. (?x)), so (number ?x)
    ; will have to do:
    (number ?x)
=>
    (assert (lte ?x ?x)))


; There's no fact of type "number", and no rule produces a fact of this type,
; so this rule is useless:
(defrule d
    (number ?x)
=>
    ; Facts can only contain atomic values, so it's not possible to specify
    ; `x + 0` simbolically (i.e. (plus ?x 0)); and since (+ ?x 0) is evaluated
    ; numerically ((+ ?x 0) -> ?x), this rule ends up being equivalent to
    ; rule c.
    (assert (lte ?x (+ ?x 0))))


; There's no fact of type "plus", and no rule produces a fact of this type, so
; this rule is useless:
(defrule e
    (plus ?x ?y)
=>
    ; (+ ?x ?y) is evaluated to the same value as (+ ?y ?x), so this rule ends
    ; up asserting a fact of the form (lte ?z ?z). Not what it was intended.
    (assert (lte (+ ?x ?y) (+ ?y ?x))))


(defrule f
    ?f-1 <- (lte ?w ?y)
    ?f-2 <- (lte ?x ?z)
    (test (neq ?f-1 ?f-2)) ; so that the same fact is not matched twice
=>
    (assert (lte (+ ?w ?x) (+ ?y ?z))))


(defrule g
    (lte ?x ?y)
    (lte ?y ?z)
=>
    (assert (lte ?x ?z)))


(reset) ; so that the facts are asserted
(run 1) ; run for only one iteration, otherwise it never ends
(facts)
