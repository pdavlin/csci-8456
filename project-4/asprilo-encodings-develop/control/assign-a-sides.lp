#include "../input.lp".

% Aux predicates to represent products that are ordered and shelved, resp.
ordered(order(O),product(A),N) :- init(object(order,O),   value(line,(A,N))).
shelved(shelf(S),product(A),N) :- init(object(product,A), value(on,  (S,N))).

% Guess assignments
{ assign(R,S,P) } :- isRobot(R), isShelf(S), isStation(P).

% For each station and product, the assignment must allow for the fulfillment of the sum of
% requested quantities by all orders
orderedAtStation(A, M, P) :- isProduct(A), isStation(P),
                             M = #sum{ N, O : ordered(O,A,N), target(O,P) }.
:- orderedAtStation(A, M, P), #sum{ N,S : assign(_,S,P), shelved(S,A,N) } < M.

% Do not assign more than one robot per shelf
:- isShelf(S), #count{ R : assign(R,S,_) } > 1.

% Determine left/right x-coordinates
side(X, left) :- SX = #max{ X' : position((X',_)) },  X<=(SX+1)/2, position((X,_)).
side(X, right) :- SX = #max{ X' : position((X',_)) }, X> (SX+1)/2, position((X,_)).

% Group robots, shelve and picking stations into left & right wrt their initial x-coordinates
right_shelves(S) :- position(S,(X,_),0), side(X,right).
left_shelves(S) :- position(S,(X,_),0), side(X,left).
right_pick(P) :- position(P,(X,_)), side(X,right).
left_pick(P) :- position(P,(X,_)), side(X,left).
right_group(R) :- position(R,(X,_),0), side(X, right).
left_group(R) :- position(R,(X,_),0), side(X, left).

% Restrict movement of left/right robots to the respective half of the grid


:- assign(R,S,_), right_group(R), left_shelves(S).
:- assign(R,S,_), left_group(R), right_shelves(S).
:- assign(R,_,P), right_group(R), left_pick(P).
:- assign(R,_,P), left_group(R), right_pick(P).

distance(R,S,|X-X'|+|Y-Y'|) :- position(R,(X,Y),0), position(S,(X',Y'),0), isRobot(R), isShelf(S).
distance(S,P,|X-X'|+|Y-Y'|) :- position(S,(X,Y),0), position(P,(X',Y')),   isShelf(S), isStation(P).

#minimize { D+D'@0,R,S,P : assign(R,S,P), distance(R,S,D), distance(S,P,D') }.


% Use all robots
:- isRobot(R), not assign(R,_,_).

% Output
#show assign/3.
#show init/2.