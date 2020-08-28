% Load this knowledge base from the command line with:
% ?- ['parcial3_punto2.pl'].

lte(0, 3).
lte(7, 9).
lte(X, X).
lte(X, plus(X, 0)).
lte(plus(X, Y), plus(Y, X)).
lte(plus(W, X), plus(Y, Z)) :- lte(W, Y), lte(X, Z).
lte(X, Z) :- lte(X, Y), lte(Y, Z).

% Execute this query from the command line:
%?- lte(plus(0, 7), plus(3, 9)).
