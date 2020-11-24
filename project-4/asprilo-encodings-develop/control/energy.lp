time(1..horizon).
% - Input conversion -------------------------------------------------------------------------------
%   Map init(object(robot, R), value(energy, E)) to internal representation,
%   .e.g energy(Robot,EnergyLevel,TimeStep)
energy(robot(R),E,1) :- init(object(robot, R), value(energy, E)).

% - Energy consumption -----------------------------------------------------------------------------

% *Generalize consumption*
% Map different actions to general consumption atoms, e.g. consume(Robot, EnergyAmount, TimeStep)
consume(R,1,T)  :- isRobot(R), time(T), move(R, _, T), not carries(R, _,T).
consume(R,2,T)  :- isRobot(R), time(T), move(R, _, T), carries(R, _,T).
consume(R,1,T)  :- isRobot(R), time(T), pickup(R, _, T).
consume(R,1,T)  :- isRobot(R), time(T), putdown(R, _, T).

% *Consumption effect*
% For each robot and time step, reflect the effect of its current consumption (via consume/3)
% towards its current energy level (via energy/3)
energy(R, E', T') :- time(T), isRobot(R), energy(R, E, T), consume(R, X, T), T'=T+1, E'=E-X.


% *Inertia*
% For each robot and time step, if no energy is currently consumed, the energy level
% remains unchanged.
energy(robot(R), E', T') :- time(T), isRobot(R), energy(robot(R), E, T), T'=T+1, E'=E, not consume(R, 1, T), not consume(R, 2, T).

% *Forbid Over-Consumption*
% For each robot and time step, the energy level must not be negative.
:- energy(robot(R), E, T), E < 0, time(T), isRobot(R).

% - Output -----------------------------------------------------------------------------------------

#show energy/3.