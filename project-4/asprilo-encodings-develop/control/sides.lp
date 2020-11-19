#include "../input.lp".

% Determine left/right x-coordinates
side(X, left) :- SX = #max{ X' : position((X',_)) },  X<=(SX+1)/2, position((X,_)).
side(X, right) :- SX = #max{ X' : position((X',_)) }, X> (SX+1)/2, position((X,_)).

% Group robots into left/right side wrt their initial position
right_group(R) :- position(R,(X,_),1), side(X, right).
left_group(R) :- position(R,(X,_),1), side(X, left).

% Forbid robots to occupy a position on the other side
:- right_group(R), moveto(C',C,T), side(C, left).
:- left_group(R), moveto(C',C,T), side(C, right).