(define
 (problem pfile_25_050)

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
           o31
           o32
           o33
           o34
           o35
           o36
           o37
           o38
           o39
           o40
           o41
           o42
           o43
           o44
           o45
           o46
           o47
           o48
           o49
           o50
           - PACKAGE
           c
           r1
           r2
           r3
           r4
           r5
           r6
           r7
           r8
           r9
           r10
           r11
           r12
           r13
           r14
           r15
           r16
           r17
           r18
           r19
           r20
           r21
           r22
           r23
           r24
           r25
           - ROOM
           d023
           d010
           d423
           d34
           d322
           d810
           d820
           d2025
           d1425
           d110
           d019
           d013
           d318
           d2425
           d1623
           d1617
           d1216
           d517
           d218
           d912
           d1119
           d1121
           d721
           d1523
           d624
           - ROOMDOOR)
 (:init
  (rloc c)
  (armempty)
  (door c r10 d010)
  (door c r13 d013)
  (door c r19 d019)
  (door c r23 d023)
  (door r1 r10 d110)
  (door r2 r18 d218)
  (door r3 r4 d34)
  (door r3 r18 d318)
  (door r3 r22 d322)
  (door r4 r3 d34)
  (door r4 r23 d423)
  (door r5 r17 d517)
  (door r6 r24 d624)
  (door r7 r21 d721)
  (door r8 r10 d810)
  (door r8 r20 d820)
  (door r9 r12 d912)
  (door r10 c d010)
  (door r10 r1 d110)
  (door r10 r8 d810)
  (door r11 r19 d1119)
  (door r11 r21 d1121)
  (door r12 r9 d912)
  (door r12 r16 d1216)
  (door r13 c d013)
  (door r14 r25 d1425)
  (door r15 r23 d1523)
  (door r16 r12 d1216)
  (door r16 r17 d1617)
  (door r16 r23 d1623)
  (door r17 r5 d517)
  (door r17 r16 d1617)
  (door r18 r2 d218)
  (door r18 r3 d318)
  (door r19 c d019)
  (door r19 r11 d1119)
  (door r20 r8 d820)
  (door r20 r25 d2025)
  (door r21 r7 d721)
  (door r21 r11 d1121)
  (door r22 r3 d322)
  (door r23 c d023)
  (door r23 r4 d423)
  (door r23 r15 d1523)
  (door r23 r16 d1623)
  (door r24 r6 d624)
  (door r24 r25 d2425)
  (door r25 r14 d1425)
  (door r25 r20 d2025)
  (door r25 r24 d2425)
  (closed d423)
  (closed d34)
  (closed d322)
  (closed d810)
  (closed d820)
  (closed d019)
  (closed d013)
  (closed d2425)
  (closed d1216)
  (closed d517)
  (closed d218)
  (closed d912)
  (closed d1119)
  (closed d1121)
  (closed d721)
  (in o1 r11)
  (in o2 r25)
  (in o3 r2)
  (in o4 r1)
  (in o5 r12)
  (in o6 r9)
  (in o7 r20)
  (in o8 r8)
  (in o9 r7)
  (in o10 r19)
  (in o11 r17)
  (in o12 r21)
  (in o13 r10)
  (in o14 r10)
  (in o15 r22)
  (in o16 r17)
  (in o17 r21)
  (in o18 r17)
  (in o19 r11)
  (in o20 r7)
  (in o21 r23)
  (in o22 r21)
  (in o23 r19)
  (in o24 r16)
  (in o25 r4)
  (in o26 r22)
  (in o27 r17)
  (in o28 r3)
  (in o29 r10)
  (in o30 r12)
  (in o31 r8)
  (in o32 r23)
  (in o33 r4)
  (in o34 r8)
  (in o35 r16)
  (in o36 r25)
  (in o37 r1)
  (in o38 r20)
  (in o39 r15)
  (in o40 r8)
  (in o41 r5)
  (in o42 r11)
  (in o43 r17)
  (in o44 r10)
  (in o45 r11)
  (in o46 r20)
  (in o47 r16)
  (in o48 r24)
  (in o49 r12)
  (in o50 r18)

(goal_in o1 r6)
         (goal_in o2 r13)
         (goal_in o3 r12)
         (goal_in o4 r7)
         (goal_in o5 r6)
         (goal_in o6 r22)
         (goal_in o7 r7)
         (goal_in o8 r14)
         (goal_in o9 r3)
         (goal_in o10 r22)
         (goal_in o11 r11)
         (goal_in o12 r14)
         (goal_in o13 r22)
         (goal_in o14 r20)
         (goal_in o15 r6)
         (goal_in o16 r24)
         (goal_in o17 r6)
         (goal_in o18 r12)
         (goal_in o19 r5)
         (goal_in o20 r4)
         (goal_in o21 r22)
         (goal_in o22 r10)
         (goal_in o23 r5)
         (goal_in o24 r17)
         (goal_in o25 r6)
         (goal_in o26 r14)
         (goal_in o27 r22)
         (goal_in o28 r24)
         (goal_in o29 r22)
         (goal_in o30 r19)
         (goal_in o31 r4)
         (goal_in o32 r23)
         (goal_in o33 r4)
         (goal_in o34 r19)
         (goal_in o35 r18)
         (goal_in o36 r1)
         (goal_in o37 r3)
         (goal_in o38 r22)
         (goal_in o39 r7)
         (goal_in o40 r3)
         (goal_in o41 r24)
         (goal_in o42 r17)
         (goal_in o43 r24)
         (goal_in o44 r18)
         (goal_in o45 r8)
         (goal_in o46 r23)
         (goal_in o47 r5)
         (goal_in o48 r15)
         (goal_in o49 r10)
         (goal_in o50 r13))

 (:goal (and
         (in o1 r6)
         (in o2 r13)
         (in o3 r12)
         (in o4 r7)
         (in o5 r6)
         (in o6 r22)
         (in o7 r7)
         (in o8 r14)
         (in o9 r3)
         (in o10 r22)
         (in o11 r11)
         (in o12 r14)
         (in o13 r22)
         (in o14 r20)
         (in o15 r6)
         (in o16 r24)
         (in o17 r6)
         (in o18 r12)
         (in o19 r5)
         (in o20 r4)
         (in o21 r22)
         (in o22 r10)
         (in o23 r5)
         (in o24 r17)
         (in o25 r6)
         (in o26 r14)
         (in o27 r22)
         (in o28 r24)
         (in o29 r22)
         (in o30 r19)
         (in o31 r4)
         (in o32 r23)
         (in o33 r4)
         (in o34 r19)
         (in o35 r18)
         (in o36 r1)
         (in o37 r3)
         (in o38 r22)
         (in o39 r7)
         (in o40 r3)
         (in o41 r24)
         (in o42 r17)
         (in o43 r24)
         (in o44 r18)
         (in o45 r8)
         (in o46 r23)
         (in o47 r5)
         (in o48 r15)
         (in o49 r10)
         (in o50 r13)))
)
