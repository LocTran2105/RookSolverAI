"""
Belief-state search for 8 Rooks problem
Search in belief space - handles uncertainty about board state
"""
import time
from collections import deque

class BeliefStateSolver:
    def __init__(self, n=8):
        self.n = n
        self.steps = 0
    
    def is_safe(self, board, row, col):
        """Check if placing a rook at (row, col) is safe"""
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def get_possible_states(self, belief_state):
        """
        Get all possible next states from current belief state
        Belief state is a set of possible board configurations
        """
        next_states = set()
        
        for state in belief_state:
            row = len([x for x in state if x != -1])
            
            if row >= self.n:
                next_states.add(state)
                continue
            
            for col in range(self.n):
                if self.is_safe(state, row, col):
                    new_state = list(state)
                    new_state[row] = col
                    next_states.add(tuple(new_state))
        
        return next_states
    
    def is_goal_belief(self, belief_state):
        """Check if any state in belief set is a goal state"""
        for state in belief_state:
            if all(x != -1 for x in state) and len(state) == self.n:
                return True, state
        return False, None
    
    def solve(self, callback=None, first_position=None):
        """
        Solve 8 Rooks problem using Belief-state search
        
        Args:
            callback: Function to call for UI updates
            first_position: Tuple (row, col) for first rook placement
        
        Returns:
            (solution, steps, time_taken)
        """
        start_time = time.time()
        self.steps = 0
        
        # Initial belief state - all possible initial configurations
        if first_position:
            row, col = first_position
            initial_state = [-1] * self.n
            initial_state[row] = col
            belief_state = {tuple(initial_state)}
            
            if callback:
                callback([col], self.steps)
        else:
            initial_state = tuple([-1] * self.n)
            belief_state = {initial_state}
        
        # BFS in belief space
        queue = deque([belief_state])
        visited = set()
        visited.add(frozenset(belief_state))
        
        while queue:
            current_belief = queue.popleft()
            self.steps += 1
            
            # Check if goal is reached
            is_goal, solution = self.is_goal_belief(current_belief)
            if is_goal:
                end_time = time.time()
                if callback:
                    callback(list(solution), self.steps)
                return list(solution), self.steps, end_time - start_time
            
            # Generate next belief states
            next_belief = self.get_possible_states(current_belief)
            
            # Update UI with one of the states
            if next_belief and callback:
                sample_state = next(iter(next_belief))
                valid_positions = [x for x in sample_state if x != -1]
                if valid_positions:
                    callback(valid_positions, self.steps)
            
            belief_key = frozenset(next_belief)
            if belief_key not in visited:
                visited.add(belief_key)
                queue.append(next_belief)
            
            # Limit search to prevent infinite loops
            if self.steps > 10000:
                break
        
        end_time = time.time()
        return None, self.steps, end_time - start_time
