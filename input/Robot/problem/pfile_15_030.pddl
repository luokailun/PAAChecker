(define
 (problem pfile_15_030)

 (:domain robot)

 (:objects o1
           o2
           o3
           o4
           o5
           o6
           o7
           o8
           o9
           o10
           o11
           o12
           o13
           o14
           o15
           o16
           o17
           o18
           o19
           o20
           o21
           o22
           o23
           o24
           o25
           o26
           o27
           o28
           o29
           o30
           - PACKAGE
           c r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 r12 r13 r14 r15 - ROOM
           d511
           d57
           d211
           d1114
           d414
           d614
           d410
           d310
           d114
           d014
           d215
           d59
           d913
           d89
           d112
           - ROOMDOOR)
 (:init
  (rloc c)
  (armempty)
  (door c r14 d014)
  (door r1 r12 d112)
  (door r1 r14 d114)
  (door r2 r11 d211)
  (door r2 r15 d215)
  (door r3 r10 d310)
  (door r4 r10 d410)
  (door r4 r14 d414)
  (door r5 r7 d57)
  (door r5 r9 d59)
  (door r5 r11 d511)
  (door r6 r14 d614)
  (door r7 r5 d57)
  (door r8 r9 d89)
  (door r9 r5 d59)
  (door r9 r8 d89)
  (door r9 r13 d913)
  (door r10 r3 d310)
  (door r10 r4 d410)
  (door r11 r2 d211)
  (door r11 r5 d511)
  (door r11 r14 d1114)
  (door r12 r1 d112)
  (door r13 r9 d913)
  (door r14 c d014)
  (door r14 r1 d114)
  (door r14 r4 d414)
  (door r14 r6 d614)
  (door r14 r11 d1114)
  (door r15 r2 d215)
  (closed d57)
  (closed d211)
  (closed d614)
  (closed d310)
  (closed d59)
  (closed d913)
  (in o1 r7)
  (in o2 r2)
  (in o3 r6)
  (in o4 r8)
  (in o5 r4)
  (in o6 r13)
  (in o7 r13)
  (in o8 r15)
  (in o9 r6)
  (in o10 r4)
  (in o11 r8)
  (in o12 r1)
  (in o13 r2)
  (in o14 r14)
  (in o15 r15)
  (in o16 r6)
  (in o17 r3)
  (in o18 r8)
  (in o19 r2)
  (in o20 r5)
  (in o21 r6)
  (in o22 r12)
  (in o23 r8)
  (in o24 r11)
  (in o25 r6)
  (in o26 r1)
  (in o27 r9)
  (in o28 r8)
  (in o29 r10)
  (in o30 r13)
(goal_in o1 r15)
         (goal_in o2 r2)
         (goal_in o3 r2)
         (goal_in o4 r8)
         (goal_in o5 r7)
         (goal_in o6 r8)
         (goal_in o7 r4)
         (goal_in o8 r14)
         (goal_in o9 r11)
         (goal_in o10 r6)
         (goal_in o11 r2)
         (goal_in o12 r7)
         (goal_in o13 r14)
         (goal_in o14 r11)
         (goal_in o15 r14)
         (goal_in o16 r12)
         (goal_in o17 r4)
         (goal_in o18 r2)
         (goal_in o19 r10)
         (goal_in o20 r4)
         (goal_in o21 r12)
         (goal_in o22 r3)
         (goal_in o23 r1)
         (goal_in o24 r4)
         (goal_in o25 r2)
         (goal_in o26 r11)
         (goal_in o27 r12)
         (goal_in o28 r2)
         (goal_in o29 r14)
         (goal_in o30 r11))

 (:goal (and
         (in o1 r15)
         (in o2 r2)
         (in o3 r2)
         (in o4 r8)
         (in o5 r7)
         (in o6 r8)
         (in o7 r4)
         (in o8 r14)
         (in o9 r11)
         (in o10 r6)
         (in o11 r2)
         (in o12 r7)
         (in o13 r14)
         (in o14 r11)
         (in o15 r14)
         (in o16 r12)
         (in o17 r4)
         (in o18 r2)
         (in o19 r10)
         (in o20 r4)
         (in o21 r12)
         (in o22 r3)
         (in o23 r1)
         (in o24 r4)
         (in o25 r2)
         (in o26 r11)
         (in o27 r12)
         (in o28 r2)
         (in o29 r14)
         (in o30 r11)))
)