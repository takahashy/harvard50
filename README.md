# Harvard CS50 - Intro to AI
## 1. Search
- Various algorithms for search
    - breadth first search (queue)
    - depth first search (stack)
- For a two player game usually use `minimax algorithm` (determines the best action 
  that a player can take based on the opponent's action)
    - one player wants to maximize their `utility` (outcome of the state)
    - other player wants to minimize their utility
    - the action that the player takes is dependent on the other player
    ```
    Maximize(state):
        value = -infinity

        if terminal state
            return the utility of that state

        for every action in player's Actions(state)
            value = max(value, value of Minimize(Result(state, action)))

        return value and action
    ```
    ```
    Minimize(state):
        value = infinity

        if terminal state
            return the utility of that state

        for every action in player's Actions(state)
            value = max(value, value of Maximize(Result(state, action)))

        return value and action
    ```
    - 2 ways to optimize the algorithm
        1. `alpha-beta pruning`: after evaluating the utility of an action, if there
            is evidence that the following action will return a better score than 
            the already taken action, there is no need to further investigate this action 
        2. `Depth limit minimax`: limit the number of steps to check in each action
           so does not reach a terminal state. Doesn't give a precise value for the
           utility of the current state so use an `evaluation function` to estimate 
           the utility of the current state. The better this function the better the
           minimax algorithm

## 2. Knowledge
- `model`: assignment of a truth value to every proposition
- `knowledge base`: a set of sentences that is known by the agent
- `entailment`: if alpha entails beta, then when alpha is true, beta is also true
- to determine if a knowledge base entails a certain query, there are several algorithms
    1. `model checking`
        - enumerate all possible models
        - if in every model, the knowledge base is true and alpha is true, then the
          knowledge base entails alpha
    2. `inference by resolution`
        - proof by contradiction
        - assume that the knowledge base and not alpha is true.
        - convert it to conjuctive normal form and see if you can use resolution to produce a new clause
            - if empty clause then contradiction
            - otherwise knowledge base does not entail alpha

- `inference rules`: given a premise, a conclusion can be made
    1. `And elimination`: if alpha and beta are true --> alpha is true (beta is true)
    2. `Double negation elimination`: if not not alpha --> alpha
    3. `Implication elimination`: if alpha then beta --> not alpha or beta
    4.  `Biconditional elimination`: alpha iff beta --> if alpha then beta AND if beta then alpha