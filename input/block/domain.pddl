(define (domain blocks)



  (:types BLOCK)

  (:predicates
    (hand-empty)
    (clear ?b - BLOCK)
    (holding ?b - BLOCK)
    (on ?top - BLOCK ?bottom - BLOCK)
    (on-table ?b - BLOCK)
    (goal_on ?t - BLOCK ?b - BLOCK)
    (goal_on-table ?b - BLOCK)
    (goal_clear ?b - BLOCK)
    (done ?b - BLOCK)
    (end)
    )


  (:action mark_done
     :parameters (?b - BLOCK)
     :precondition (not (done ?b))
     :effect (done ?b)
  )


  (:action pickup
    :parameters (?b - BLOCK)
    :precondition (and (hand-empty) (clear ?b) (on-table ?b))
    :effect (and
      (not (hand-empty))
      (not (clear ?b)) 
      (not (on-table ?b))
      (holding ?b)))


  (:action putdown
    :parameters (?b - BLOCK)
    :precondition (holding ?b)
    :effect (and
      (hand-empty)
      (not (holding ?b))
      (on-table ?b) (clear ?b)))


  (:action stack
    :parameters (?top - BLOCK ?bottom - BLOCK)
    :precondition (and
      (holding ?top)
      (clear ?bottom))
    :effect (and
      (hand-empty)
      (not (holding ?top))
      (not (clear ?bottom))
      (on ?top ?bottom)
      (clear ?top)))


  (:action unstack
    :parameters (?top - BLOCK ?bottom - BLOCK)
    :precondition (and
      (hand-empty)
      (clear ?top)
      (on ?top ?bottom))
    :effect (and
      (not (hand-empty))
      (not (clear ?top))
      (not (on ?top ?bottom))
      (holding ?top)
      (clear ?bottom)))

  (:action nop
  :parameters ()
  :precondition ()
  :effect (end))


)