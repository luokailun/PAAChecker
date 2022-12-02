(define (domain robot)

  (:requirements :negative-preconditions
	:typing
  )

  (:types PACKAGE ROOM ROOMDOOR)

  (:predicates 
    (armempty)
    (rloc ?loc - ROOM) 
    (in ?obj - PACKAGE ?loc - ROOM)
    (holding ?obj - PACKAGE)
    (closed ?d - ROOMDOOR)
    (door ?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
    
    (goal_in ?obj - PACKAGE ?loc - ROOM))



(:action pickup
 :parameters (?obj - PACKAGE ?loc - ROOM)
 :precondition (and (armempty) (rloc ?loc) (in ?obj ?loc)) 
 :effect (and (not (in ?obj ?loc)) (not (armempty)) (holding ?obj))
)


(:action putdown
 :parameters (?obj - PACKAGE ?loc - ROOM)
 :precondition (and (rloc ?loc) (holding ?obj) (goal_in ?obj ?loc))
 :effect (and (not (holding ?obj)) (armempty) (in ?obj ?loc))
)


(:action move
 :parameters (?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
 :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (not (closed ?d)))
 :effect (and (rloc ?loc2) (not (rloc ?loc1)))
)


(:action open
 :parameters (?loc1 - ROOM ?loc2 - ROOM ?d - ROOMDOOR)
 :precondition (and (rloc ?loc1) (door ?loc1 ?loc2 ?d) (closed ?d))
 :effect (and (not (closed ?d)))
)
)
