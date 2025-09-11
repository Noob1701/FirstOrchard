README Contents

I. Disclaimer
II. Rules of Play
III. Simulations
IV. Solver
V. Notebook
VI. Play the Game
VII. Current Thoughts on Applications for Game Design

I. Disclaimer:

This repo is an educational project to simulate and analyze win probabilities in cooperative children’s games, inspired by First Orchard by HABA.

It is not affiliated with or endorsed by HABA, and does not use any proprietary game content. The project was built to explore real-time state evaluation for gameplay scenarios.

II. Rules of Play

Object of Game: Players play as a team to collect all the fruits before the raven reaches the end of it's track. 

Gameplay: This is a simple game. A die is rolled and then the action based on that die is taken. Four sides correspond to a particular color. And when one of these colors are rolled a fruit of that color is collected into the basket. 

One side corresponds to the raven which has five spaces on it's track. If the raven reaches the end the game is over and the players lose. 

The last side corresponds to a color of the players choice and the player collects a fruit of their choice into the basket. This is the only decision in the game and makes this game a great candidate for an initial analysis. 

III. Simulations

This repo contains code for Monte Carlo simulations and the two log files contain results of the Monte Carlo simulations against the solver. 

There are three separate simulations that are run as a result of the run batches functions. A strategy where a player picks the fruit type with the least remaining, the most remaining, and a random fruit. Simulations indicate that the best strategy is always choosing from the fruit with the most remaining. 

An intuitive explanation for this conclusion is that when you pick from fruits with less remaining you increase the odds of one fruit being empty before the othres. When a fruit is empty you are decreasing the number of good sides for you while the number of bad sides remain the same (1).


IV. Solver 

This repo analytically solves the game and confirms via simulation that the probability of winning from the starting state — assuming optimal play — is approximately 63.2%.

The solver can also compute the win probability from any given game state, and it supports comparisons between different states to evaluate how favorable one situation is versus another.

Methodology
This was implemented using a Markov Decision Process (MDP) and a recursive function. At each stage:

A die roll can produce one of six outcomes, each with a probability of 1/6.

If one of the fruit types becomes empty, its corresponding action becomes invalid — so the remaining actionable outcomes are redistributed evenly (e.g., if only 5 options remain, each has a 1/5 chance).

Each resulting state is fed back into the solver via recursion, constructing a complete probabilistic tree of outcomes.

Wild Roll Strategies
The "wild" die side allows the player to choose any remaining fruit. The solver currently supports several strategies for handling this choice:

Largest – Always pick the fruit type with the most remaining pieces

Smallest – Always pick the fruit type with the fewest remaining pieces

Random – Choose a fruit at random (Note: The random strategy is not yet fully analytically solved; it currently uses non-deterministic simulation)

These strategies are included in the recursive calculation and follow the same probabilistic branching (1/6 base probability, reduced as options become invalid).

V. Notebook

There are some simulations as well as outcomes from the solver in the montecarlo.ipynb python notebook. This notebook focuses on the starting state of the game, but gives you a feel for the process involved in solving the game. 

VI. Playing the Game 

Currently this repo has a minimally playable text based version in gameplay.py that allows the user to know what the odds are of winning after a choosing a fruit based on a wild roll. 

VII. Current Thoughts on Applications for Game Design

This repo analytically proves that the win rate for this chidlren's game is 63.2% (less if a toddler just picks their favorite color all the time). 

As a parent I think this is a little low for a children's game. I do want there to be real risk of losing otherwise the game would be pointless. But I think 75% would be more appropriate (assuming best strategy). 

And game testers with toddlers might be able to deduce a good percent win rate for the experience of families who wish to enjoy the game. 

Let's say I did want 75% to the the win rate. Then, I could easily tweak the starting conditions let's say I added one more space to the raven track. This would increase the odds of winning to approximately 76.9%. (See last line of montecarlo python notebook). The idea here is that you could easily customize your win percentage for a simple cooperative boardgame for children.

Another application comes from the Monte Carlo simulations. It is not always or even usually feasible to fully mathematically solve a game, especially with multiple players. What you can do quickly is to see how often certain scenarios pop up. 

Let's say a prototyped game has gotten negative feedback about a particular combination of cards, but the individual cards are well liked. One thought might be to tweak each card to hamper this effect. And this might be the solution. But you also might want to know how often this combination is likely to occur and under what conditions is it more likely to occur. 

In short, another way around such a game decision choice would be to limit the odds of that combination occurring. 

Also such Monte Carlo simulations and in some cases an analytical solver could check for balance in games that have some sort of asymmetry, such as different factions/characters that someone controls. Does one character or faction have a decided advantage. 

For instance, Connect 4 has an imbalance in that with perfect play the player who makes the first move will win. 

Monte Carlo methods and especially analytical solvers are more easily applied to a game of simple/moderate complexity. And I am going to continue to work on understanding what can be done and what limits there are. 