(define
 (problem pfile_04_005)

 (:domain robot)

(:objects o1 o2 o3 o4 o5 - PACKAGE
c r1 r2 r3 r4 - ROOM
d24 d04 d03 d14 - ROOMDOOR)
 (:init
(rloc c)
(armempty)
(door c r3 d03)
(door c r4 d04)
(door r1 r4 d14)
(door r2 r4 d24)
(door r3 c d03)
(door r4 c d04)
(door r4 r1 d14)
(door r4 r2 d24)
(closed d24)
(closed d04)
(in o1 r2)
(in o2 r3)
(in o3 r4)
(in o4 r2)
(in o5 r1)
(goal_in o1 r4) (goal_in o2 r4) (goal_in o3 r2) (goal_in o4 r4) (goal_in o5 r2))

 (:goal (and
	(in o1 r4) (in o2 r4) (in o3 r2) (in o4 r4) (in o5 r2)	
		))
)
