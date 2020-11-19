% - Input conversion -------------------------------------------------------------------------------
%   Map init(object(robot, R), value(energy, E)) to internal representation,
%   .e.g energy(Robot,EnergyLevel,TimeStep)
energy(robot(R),E,0) :- init(object(robot, R), value(energy, E)).

% - Energy consumption -----------------------------------------------------------------------------

% *Generalize consumption*
% Map different actions to general consumption atoms, e.g. consume(Robot, EnergyAmount, TimeStep)
consume(R,1,T)  :- move(R, _, T), not carries(R, _,T).
% consume(R,2,T)  :- move(R, _, T), carries(R, _,T).
% consume(R,1,T)  :- pickup(R, _, T).
% consume(R,1,T)  :- putdown(R, _, T).
% consume(R,0,T)  :- deliver(R, T).

% *Consumption effect*
% For each robot and time step, reflect the effect of its current consumption (via consume/3)
% towards its current energy level (via energy/3)
energy(robot(R), E', T') :- energy(robot(R), E, T), consume(R,X,T), time(T), T'=T+1, E' = E - 1.

% *Inertia*
% For each robot and time step, if no energy is currently consumed, the energy level
% remains unchanged.


% *Forbid Over-Consumption*
% For each robot and time step, the energy level must not be negative.
:- energy(robot(R), lev, T), lev < 0.

% - Output -----------------------------------------------------------------------------------------

#show energy/3.