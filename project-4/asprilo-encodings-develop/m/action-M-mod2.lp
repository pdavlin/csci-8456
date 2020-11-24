#include "../input.lp".

%#const horizon=1.
time(1..horizon).

direction((X,Y)) :- X=-1..1, Y=-1..1.
direction((X,Y)) :- X=-1..1, Y=-1..1.
nextto((X,Y),(X',Y'),(X+X',Y+Y')) :- position((X,Y)), direction((X',Y')), position((X+X',Y+Y')).

{ move(R,D,T) : direction(D) } 1 :- isRobot(R), time(T).

% - move/3 ----------------------------------------------------------------------
position(R,C,T) :- move(R,D,T), position(R,C',T-1),     nextto(C',D,C).
                :- move(R,D,T), position(R,C ,T-1), not nextto(C ,D,_).

% - inertia ---------------------------------------------------------------------
position(R,C,T) :- position(R,C,T-1), not move(R,_,T), isRobot(R), time(T).

% - edge collision --------------------------------------------------------------
% some robot is moving from coordinate C' to coordinate C at time T
moveto(C',C,T) :- nextto(C',D,C), position(R,C',T-1), move(R,D,T).
 :- moveto(C',C,T), moveto(C,C',T), C < C'.


 :- moveto((X',Y'),(X,Y),T), moveto((X1',Y1'),(X1,Y1),T), |X-X'| = 1, X = X1, X' = X1', Y' = Y1, Y = Y1'.
 :- moveto((X',Y'),(X,Y),T), moveto((X1',Y1'),(X1,Y1),T), |Y-Y'| = 1, Y = Y1, Y' = Y1', X' = X1, X = X1'.

% - vertex collision ------------------------------------------------------------
 :- { position(R,C,T) : isRobot(R) }  > 1, position(C), time(T).

% - auxiliaries -----------------------------------------------------------------
 :- { position(R,C,T) } != 1, isRobot(R), time(T).    % REDUNDANT but PERFORMANT?
