import copy
import heapq
import math
import time
from collections import deque
import tkinter as tk
from tkinter import messagebox, ttk
import random

# ------------------------- Puzzle State Representation -------------------------
class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0, cost=0):
        self.board = board  # 1D list of 9 elements
        self.parent = parent
        self.move = move  # move made to reach this state
        self.depth = depth
        self.cost = cost  # g(n) for A*
        self.zero_index = board.index(0)

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(self.board))

    def __lt__(self, other):
        return self.cost < other.cost

    def is_goal(self):
        return self.board == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def get_neighbors(self):
        neighbors = []
        x, y = self.zero_index % 3, self.zero_index // 3
        moves = [('Up', 0, -1), ('Down', 0, 1), ('Left', -1, 0), ('Right', 1, 0)]

        for move_name, dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_zero_index = new_y * 3 + new_x
                new_board = copy.deepcopy(self.board)
                new_board[self.zero_index], new_board[new_zero_index] = new_board[new_zero_index], new_board[self.zero_index]
                neighbors.append(PuzzleState(new_board, self, move_name, self.depth + 1, self.cost + 1))
        return neighbors

    def print_board(self):
        for i in range(0, 9, 3):
            print(self.board[i:i+3])
        print()

# ------------------------- Heuristics for A* -------------------------
def manhattan_heuristic(state):
    """Manhattan distance heuristic"""
    total = 0
    for i, val in enumerate(state.board):
        if val != 0:
            goal_index = val
            current_x, current_y = i % 3, i // 3
            goal_x, goal_y = goal_index % 3, goal_index // 3
            total += abs(current_x - goal_x) + abs(current_y - goal_y)
    return total

def euclidean_heuristic(state):
    """Euclidean distance heuristic"""
    total = 0
    for i, val in enumerate(state.board):
        if val != 0:
            goal_index = val
            current_x, current_y = i % 3, i // 3
            goal_x, goal_y = goal_index % 3, goal_index // 3
            total += math.sqrt((current_x - goal_x)**2 + (current_y - goal_y)**2)
    return total

# ------------------------- BFS (Standard) -------------------------
def bfs(initial_state):
    frontier = deque([initial_state])
    explored = set()
    nodes_expanded = 0
    start_time = time.time()
    max_frontier_size = 0

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        state = frontier.popleft()
        explored.add(state)
        nodes_expanded += 1

        if state.is_goal():
            return state, nodes_expanded, time.time() - start_time, max_frontier_size

        for neighbor in state.get_neighbors():
            if neighbor not in explored and neighbor not in frontier:
                frontier.append(neighbor)
    
    return None, nodes_expanded, time.time() - start_time, max_frontier_size

# ------------------------- DFS (Standard with depth limit) -------------------------
def dfs(initial_state, max_depth=1000):
    frontier = [initial_state]
    explored = set()
    nodes_expanded = 0
    start_time = time.time()
    max_frontier_size = 0

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        state = frontier.pop()
        
        if state.depth > max_depth:
            continue
        if state in explored:
            continue
            
        explored.add(state)
        nodes_expanded += 1

        if state.is_goal():
            return state, nodes_expanded, time.time() - start_time, max_frontier_size

        neighbors = state.get_neighbors()
        for neighbor in reversed(neighbors):
            if neighbor not in explored and neighbor not in frontier:
                frontier.append(neighbor)
    
    return None, nodes_expanded, time.time() - start_time, max_frontier_size

# ------------------------- Limited DFS (Iterative Deepening) -------------------------
def limited_dfs(initial_state, depth_limit):
    frontier = [initial_state]
    explored = set()
    nodes_expanded = 0
    
    while frontier:
        state = frontier.pop()
        
        if state.depth > depth_limit:
            continue
        if state in explored:
            continue
            
        explored.add(state)
        nodes_expanded += 1
        
        if state.is_goal():
            return state, nodes_expanded, True
        
        neighbors = state.get_neighbors()
        for neighbor in reversed(neighbors):
            if neighbor not in explored:
                frontier.append(neighbor)
    
    return None, nodes_expanded, False

def iterative_deepening_dfs(initial_state, max_depth=50):
    start_time = time.time()
    total_nodes_expanded = 0
    
    for depth in range(max_depth + 1):
        goal_state, nodes_expanded, found = limited_dfs(initial_state, depth)
        total_nodes_expanded += nodes_expanded
        
        if found:
            return goal_state, total_nodes_expanded, time.time() - start_time
    
    return None, total_nodes_expanded, time.time() - start_time

# ------------------------- A* Search -------------------------
def a_star(initial_state, heuristic):
    open_set = []
    initial_f = heuristic(initial_state)
    heapq.heappush(open_set, (initial_f, id(initial_state), initial_state))
    
    g_score = {initial_state: 0}
    f_score = {initial_state: initial_f}
    
    explored = set()
    nodes_expanded = 0
    start_time = time.time()
    max_frontier_size = 0

    while open_set:
        max_frontier_size = max(max_frontier_size, len(open_set))
        _, _, current = heapq.heappop(open_set)
        
        if current in explored:
            continue
            
        explored.add(current)
        nodes_expanded += 1

        if current.is_goal():
            return current, nodes_expanded, time.time() - start_time, max_frontier_size

        for neighbor in current.get_neighbors():
            tentative_g = current.depth + 1
            
            if tentative_g < g_score.get(neighbor, float('inf')):
                neighbor.parent = current
                neighbor.depth = tentative_g
                neighbor.cost = tentative_g
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor)
                
                if neighbor not in explored:
                    heapq.heappush(open_set, (f_score[neighbor], id(neighbor), neighbor))
    
    return None, nodes_expanded, time.time() - start_time, max_frontier_size

# ------------------------- Path Reconstruction -------------------------
def reconstruct_path(state):
    path = []
    moves = []
    while state.parent:
        path.append(state)
        moves.append(state.move)
        state = state.parent
    path.append(state)
    return list(reversed(path)), list(reversed(moves))

# ------------------------- Check Solvability -------------------------
def is_solvable(board):
    inversion_count = 0
    flat_board = [x for x in board if x != 0]
    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] > flat_board[j]:
                inversion_count += 1
    return inversion_count % 2 == 0

def generate_random_state():
    """Generate a random solvable puzzle state"""
    while True:
        board = list(range(9))
        random.shuffle(board)
        if is_solvable(board):
            return board


# ===================== TERMINAL OUTPUT FUNCTIONS (ADDED) =====================

def print_terminal_header():
    """Print header for terminal output"""
    print("\n" + "="*80)
    print("                   8-PUZZLE SOLVER - TERMINAL OUTPUT")
    print("="*80)
    print("\n NOTE: This output shows results for the FIXED initial state: [1, 2, 5, 3, 4, 0, 6, 7, 8]")
    print("         The GUI below will allow you to test random puzzles interactively.\n")
    print("="*80)

def print_initial_state_terminal(board):
    """Print initial state visualization"""
    print("\n📍 INITIAL STATE:")
    print("-" * 40)
    for i in range(0, 9, 3):
        print(f"   {board[i]}   {board[i+1]}   {board[i+2]}")
    print("-" * 40)

def print_goal_state_terminal():
    """Print goal state visualization"""
    print("\n🎯 GOAL STATE:")
    print("-" * 40)
    print("   0   1   2")
    print("   3   4   5")
    print("   6   7   8")
    print("-" * 40)

def print_solution_steps_terminal(path, moves, algorithm_name):
    """Print detailed solution steps"""
    print(f"\n{'='*80}")
    print(f"📊 {algorithm_name} - SOLUTION DETAILS")
    print(f"{'='*80}")
    
    print(f"\n✅ Path to goal (moves): {' → '.join(moves)}")
    print(f"💰 Cost of path: {len(moves)} steps")
    print(f"📈 Search depth: {len(moves)}")
    
    print(f"\n{'─'*80}")
    print("📋 DETAILED STEPS VISUALIZATION:")
    print(f"{'─'*80}")
    
    for i, state in enumerate(path):
        print(f"\n📍 Step {i}:")
        if state.move:
            print(f"   Move: {state.move}")
        print("   ┌─────┬─────┬─────┐")
        for row in range(3):
            row_str = "   │"
            for col in range(3):
                val = state.board[row*3 + col]
                if val == 0:
                    row_str += "  ●  │"
                else:
                    row_str += f"  {val}  │"
            print(row_str)
            if row < 2:
                print("   ├─────┼─────┼─────┤")
        print("   └─────┴─────┴─────┘")
    print(f"\n{'─'*80}")

def print_algorithm_result_terminal(algorithm_name, goal_state, nodes_expanded, runtime, max_frontier, heuristic_name=""):
    """Print results for a single algorithm"""
    if goal_state is None:
        print(f"\n❌ {algorithm_name} {heuristic_name}: NO SOLUTION FOUND!")
        print(f"   Nodes expanded: {nodes_expanded}")
        print(f"   Time: {runtime:.6f} seconds")
        return
    
    path, moves = reconstruct_path(goal_state)
    
    print(f"\n{'='*80}")
    print(f"🎯 {algorithm_name} {heuristic_name}")
    print(f"{'='*80}")
    print(f"   ✅ Solution Found!")
    print(f"   📍 Path to goal: {' → '.join(moves)}")
    print(f"   💰 Cost of path: {len(moves)} steps")
    print(f"   🔍 Nodes expanded: {nodes_expanded}")
    print(f"   ⏱️  Running time: {runtime:.6f} seconds")
    print(f"   📊 Max frontier size: {max_frontier}")
    print(f"   📈 Search depth: {goal_state.depth}")

def print_comparison_table_terminal(results):
    """Print comparison table of all algorithms"""
    print(f"\n{'='*80}")
    print("                    📊 COMPARISON SUMMARY")
    print(f"{'='*80}")
    print(f"\n{'Algorithm':<22} {'Steps':<8} {'Nodes Expanded':<16} {'Time (s)':<12} {'Max Frontier':<12}")
    print("-" * 80)
    
    for name, (goal_state, nodes_expanded, runtime, max_frontier) in results.items():
        if goal_state:
            steps = goal_state.depth
            print(f"{name:<22} {steps:<8} {nodes_expanded:<16} {runtime:<12.6f} {max_frontier:<12}")
        else:
            print(f"{name:<22} {'N/A':<8} {nodes_expanded:<16} {runtime:<12.6f} {max_frontier:<12}")
    print("-" * 80)

def print_heuristic_conclusion_terminal(results):
    """Print conclusion about which heuristic is more admissible"""
    print(f"\n{'='*80}")
    print("                    💡 CONCLUSION: Which Heuristic is More Admissible?")
    print(f"{'='*80}")
    
    manhattan_result = results.get('A* Manhattan', (None, 0, 0, 0))
    euclidean_result = results.get('A* Euclidean', (None, 0, 0, 0))
    
    manhattan_goal = manhattan_result[0]
    euclidean_goal = euclidean_result[0]
    manhattan_nodes = manhattan_result[1]
    euclidean_nodes = euclidean_result[1]
    
    if manhattan_goal and euclidean_goal:
        print("\n   📌 Both heuristics found the optimal solution.")
        print(f"\n   📊 Node Expansion Comparison:")
        print(f"      • Manhattan Heuristic: {manhattan_nodes} nodes expanded")
        print(f"      • Euclidean Heuristic: {euclidean_nodes} nodes expanded")
        
        if manhattan_nodes <= euclidean_nodes:
            print("\n   ✅ CONCLUSION: MANHATTAN HEURISTIC is MORE ADMISSIBLE")
            print("      → It expands fewer or equal nodes than Euclidean heuristic")
            print("      → Provides tighter lower bounds for the 8-puzzle")
        else:
            print("\n   ✅ CONCLUSION: EUCLIDEAN HEURISTIC is MORE ADMISSIBLE")
            print("      → It expands fewer nodes than Manhattan heuristic")
    
    print("\n   💡 Why Manhattan is generally better for 8-Puzzle:")
    print("      • Manhattan distance exactly matches the movement constraints")
    print("      • Tiles can only move horizontally/vertically")
    print("      • Euclidean distance can underestimate (e.g., diagonal moves)")
    print("      • Tighter heuristic = more efficient search")
    print(f"\n{'='*80}")

def run_terminal_tests():
    """Run all algorithms on the fixed initial state and print results to terminal"""
    
    # Fixed initial state from assignment
    initial_board = [1, 2, 5, 3, 4, 0, 6, 7, 8]
    
    # Print header
    print_terminal_header()
    
    # Print initial and goal states
    print_initial_state_terminal(initial_board)
    print_goal_state_terminal()
    
    # Check solvability
    print(f"\n🔍 CHECKING SOLVABILITY:")
    print("-" * 40)
    if is_solvable(initial_board):
        print("   ✅ This puzzle configuration is SOLVABLE (even inversion count)")
    else:
        print("   ❌ This puzzle configuration is UNSOLVABLE (odd inversion count)")
        return
    
    # Create initial state
    initial_state = PuzzleState(initial_board)
    
    # Dictionary to store results
    results = {}
    
    # Run BFS
    print("\n" + "🔄" * 40)
    print("   RUNNING BREADTH-FIRST SEARCH (BFS)")
    print("🔄" * 40)
    goal, nodes_exp, runtime, max_front = bfs(initial_state)
    results['BFS'] = (goal, nodes_exp, runtime, max_front)
    if goal:
        path, moves = reconstruct_path(goal)
        print_solution_steps_terminal(path, moves, "BFS")
    print_algorithm_result_terminal("BFS", goal, nodes_exp, runtime, max_front)
    
    # Run DFS
    print("\n" + "🔄" * 40)
    print("   RUNNING DEPTH-FIRST SEARCH (DFS) - Depth Limit: 1000")
    print("🔄" * 40)
    goal, nodes_exp, runtime, max_front = dfs(initial_state)
    results['DFS'] = (goal, nodes_exp, runtime, max_front)
    if goal:
        path, moves = reconstruct_path(goal)
        print_solution_steps_terminal(path, moves, "DFS")
    print_algorithm_result_terminal("DFS", goal, nodes_exp, runtime, max_front)
    
    # Run IDDFS
    print("\n" + "🔄" * 40)
    print("   RUNNING ITERATIVE DEEPENING DFS (IDDFS)")
    print("🔄" * 40)
    goal, nodes_exp, runtime = iterative_deepening_dfs(initial_state)
    results['IDDFS'] = (goal, nodes_exp, runtime, 0)
    if goal:
        path, moves = reconstruct_path(goal)
        print_solution_steps_terminal(path, moves, "IDDFS")
    print_algorithm_result_terminal("IDDFS", goal, nodes_exp, runtime, 0)
    
    # Run A* with Manhattan
    print("\n" + "🔄" * 40)
    print("   RUNNING A* SEARCH with MANHATTAN HEURISTIC")
    print("🔄" * 40)
    goal, nodes_exp, runtime, max_front = a_star(initial_state, manhattan_heuristic)
    results['A* Manhattan'] = (goal, nodes_exp, runtime, max_front)
    if goal:
        path, moves = reconstruct_path(goal)
        print_solution_steps_terminal(path, moves, "A* Manhattan")
    print_algorithm_result_terminal("A* Manhattan", goal, nodes_exp, runtime, max_front, "Manhattan")
    
    # Run A* with Euclidean
    print("\n" + "🔄" * 40)
    print("   RUNNING A* SEARCH with EUCLIDEAN HEURISTIC")
    print("🔄" * 40)
    goal, nodes_exp, runtime, max_front = a_star(initial_state, euclidean_heuristic)
    results['A* Euclidean'] = (goal, nodes_exp, runtime, max_front)
    if goal:
        path, moves = reconstruct_path(goal)
        print_solution_steps_terminal(path, moves, "A* Euclidean")
    print_algorithm_result_terminal("A* Euclidean", goal, nodes_exp, runtime, max_front, "Euclidean")
    
    # Print comparison table
    print_comparison_table_terminal(results)
    
    # Print conclusion
    print_heuristic_conclusion_terminal(results)
    
    # Print separator before GUI
    print("\n" + "="*80)
    print("                    🚀 LAUNCHING GRAPHICAL USER INTERFACE (GUI)")
    print("="*80)
    print("\n   The GUI below allows you to:")
    print("   • Generate random solvable puzzles")
    print("   • Run individual algorithms")
    print("   • Compare all algorithms simultaneously")
    print("   • Animate the solution step by step")
    print("\n" + "="*80 + "\n")


# ------------------------- GUI Application -------------------------
class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver - AI Search Algorithms")
        self.root.geometry("1000x750")
        self.root.configure(bg='#2c3e50')
        
        self.current_state = None
        self.solution_path = []
        self.current_step = 0
        self.animation_id = None
        self.current_results = {}  # Store results for all algorithms
        
        self.setup_gui()
        
        # Generate initial random puzzle
        self.generate_new_random_puzzle()
        
    def setup_gui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="8-Puzzle Solver", 
                               font=('Arial', 24, 'bold'), 
                               fg='#ecf0f1', bg='#2c3e50')
        title_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Left side - Puzzle display
        puzzle_container = tk.Frame(main_frame, bg='#2c3e50')
        puzzle_container.pack(side='left', padx=20, pady=20)
        
        self.puzzle_frame = tk.Frame(puzzle_container, bg='#34495e', relief='ridge', bd=3)
        self.puzzle_frame.pack()
        
        self.puzzle_cells = []
        for i in range(3):
            row = []
            for j in range(3):
                cell = tk.Label(self.puzzle_frame, text='', font=('Arial', 40, 'bold'),
                               width=4, height=2, relief='solid', bd=2,
                               bg='#ecf0f1', fg='#2c3e50')
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.puzzle_cells.append(row)
        
        # Puzzle info
        info_label = tk.Label(puzzle_container, text="Current Puzzle State", 
                             font=('Arial', 12), fg='#ecf0f1', bg='#2c3e50')
        info_label.pack(pady=5)
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#34495e', relief='ridge', bd=3)
        control_frame.pack(side='right', padx=20, pady=20, fill='both', expand=True)
        
        # Random puzzle button (main button)
        self.random_btn = tk.Button(control_frame, text="🎲 Generate Random Puzzle", 
                                   command=self.generate_new_random_puzzle,
                                   font=('Arial', 14, 'bold'),
                                   bg='#3498db', fg='white',
                                   activebackground='#2980b9',
                                   padx=20, pady=10)
        self.random_btn.pack(pady=15)
        
        # Separator
        separator = ttk.Separator(control_frame, orient='horizontal')
        separator.pack(fill='x', pady=10, padx=10)
        
        # Run all algorithms button
        self.run_all_btn = tk.Button(control_frame, text="🚀 Run All Algorithms", 
                                    command=self.run_all_algorithms,
                                    font=('Arial', 14, 'bold'),
                                    bg='#27ae60', fg='white',
                                    activebackground='#229954',
                                    padx=20, pady=10)
        self.run_all_btn.pack(pady=15)
        
        # Individual algorithm buttons
        algo_frame = tk.LabelFrame(control_frame, text="Individual Algorithms", 
                                   font=('Arial', 12, 'bold'),
                                   fg='#ecf0f1', bg='#34495e')
        algo_frame.pack(pady=10, padx=10, fill='x')
        
        algorithms = [
            ("BFS", "#3498db"),
            ("DFS", "#e74c3c"),
            ("IDDFS", "#f39c12"),
            ("A* Manhattan", "#9b59b6"),
            ("A* Euclidean", "#1abc9c")
        ]
        
        self.algo_buttons = {}
        for algo, color in algorithms:
            btn = tk.Button(algo_frame, text=f"Run {algo}", 
                           command=lambda a=algo: self.run_single_algorithm(a),
                           font=('Arial', 10),
                           bg=color, fg='white',
                           activebackground=color,
                           padx=10, pady=5)
            btn.pack(side='left', padx=5, pady=5, expand=True, fill='x')
            self.algo_buttons[algo] = btn

        # Animation controls
        anim_frame = tk.LabelFrame(control_frame, text="Solution Animation", 
                                   font=('Arial', 11, 'bold'),
                                   fg='#ecf0f1', bg='#34495e')
        anim_frame.pack(pady=10, padx=10, fill='x')
        
        self.prev_btn = tk.Button(anim_frame, text="◀ Previous", 
                                  command=self.prev_step, state='disabled',
                                  font=('Arial', 10), bg='#95a5a6')
        self.prev_btn.pack(side='left', padx=5, pady=5, expand=True)
        
        self.next_btn = tk.Button(anim_frame, text="Next ▶", 
                                  command=self.next_step, state='disabled',
                                  font=('Arial', 10), bg='#95a5a6')
        self.next_btn.pack(side='left', padx=5, pady=5, expand=True)
        
        self.animate_btn = tk.Button(anim_frame, text="▶ Animate", 
                                     command=self.animate_solution, state='disabled',
                                     font=('Arial', 10), bg='#f39c12')
        self.animate_btn.pack(side='left', padx=5, pady=5, expand=True)
        
        self.stop_btn = tk.Button(anim_frame, text="■ Stop", 
                                  command=self.stop_animation, state='disabled',
                                  font=('Arial', 10), bg='#e74c3c')
        self.stop_btn.pack(side='left', padx=5, pady=5, expand=True)
        
        # Results display with Notebook (tabs)
        results_frame = tk.LabelFrame(control_frame, text="Results", 
                                      font=('Arial', 12, 'bold'),
                                      fg='#ecf0f1', bg='#34495e')
        results_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs for each algorithm
        self.result_texts = {}
        algorithms_list = ["BFS", "DFS", "IDDFS", "A* Manhattan", "A* Euclidean"]
        
        for algo in algorithms_list:
            tab = tk.Frame(self.notebook, bg='#2c3e50')
            self.notebook.add(tab, text=algo)
            
            text_widget = tk.Text(tab, height=12, width=40, 
                                  font=('Courier', 9), 
                                  bg='#ecf0f1', fg='#2c3e50',
                                  wrap=tk.WORD)
            scrollbar = tk.Scrollbar(tab, orient='vertical', command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            text_widget.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            self.result_texts[algo] = text_widget
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready - Click 'Generate Random Puzzle' to start", 
                                   font=('Arial', 10), 
                                   bg='#7f8c8d', fg='white',
                                   relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
        
    def update_display(self):
        """Update the puzzle display"""
        if self.current_state:
            for i in range(3):
                for j in range(3):
                    value = self.current_state.board[i*3 + j]
                    if value == 0:
                        self.puzzle_cells[i][j].configure(text='', bg='#95a5a6')
                    else:
                        self.puzzle_cells[i][j].configure(text=str(value), bg='#ecf0f1')
    
    def generate_new_random_puzzle(self):
        """Generate a new random solvable puzzle"""
        if self.animation_id:
            self.stop_animation()
        
        board = generate_random_state()
        self.current_state = PuzzleState(board)
        self.solution_path = []
        self.current_step = 0
        self.current_results = {}
        
        self.update_display()
        
        # Clear all result tabs
        for algo, text_widget in self.result_texts.items():
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, f"Click 'Run All Algorithms' or 'Run {algo}' to see results...")
        
        # Disable animation buttons
        self.prev_btn.config(state='disabled')
        self.next_btn.config(state='disabled')
        self.animate_btn.config(state='disabled')
        self.stop_btn.config(state='disabled')
        
        self.status_bar.config(text=f"New random puzzle generated! (Solvable)")
        
    def reset_puzzle(self):
        """Reset to the first random puzzle generated"""
        if self.animation_id:
            self.stop_animation()
        
        if hasattr(self, 'initial_board'):
            self.current_state = PuzzleState(self.initial_board)
            self.solution_path = []
            self.current_step = 0
            self.update_display()
            self.status_bar.config(text="Reset to initial puzzle")
        
    def run_single_algorithm(self, algorithm):
        """Run a single algorithm and display results in its tab"""
        if not self.current_state:
            messagebox.showwarning("Warning", "Please generate a puzzle first!")
            return
        
        if self.animation_id:
            self.stop_animation()
        
        self.status_bar.config(text=f"Running {algorithm}... Please wait")
        self.root.update()
        
        try:
            if algorithm == "BFS":
                goal_state, nodes_expanded, runtime, max_frontier = bfs(self.current_state)
                self.display_single_result(algorithm, goal_state, nodes_expanded, runtime, max_frontier)
                
            elif algorithm == "DFS":
                goal_state, nodes_expanded, runtime, max_frontier = dfs(self.current_state)
                self.display_single_result(algorithm, goal_state, nodes_expanded, runtime, max_frontier)
                
            elif algorithm == "IDDFS":
                goal_state, nodes_expanded, runtime = iterative_deepening_dfs(self.current_state)
                self.display_single_result(algorithm, goal_state, nodes_expanded, runtime, max_frontier=0)
                
            elif algorithm == "A* Manhattan":
                goal_state, nodes_expanded, runtime, max_frontier = a_star(self.current_state, manhattan_heuristic)
                self.display_single_result(algorithm, goal_state, nodes_expanded, runtime, max_frontier)
                
            elif algorithm == "A* Euclidean":
                goal_state, nodes_expanded, runtime, max_frontier = a_star(self.current_state, euclidean_heuristic)
                self.display_single_result(algorithm, goal_state, nodes_expanded, runtime, max_frontier)
                
            self.status_bar.config(text=f"{algorithm} completed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_bar.config(text="Error occurred during solving")
    
    def display_single_result(self, algorithm, goal_state, nodes_expanded, runtime, max_frontier=0):
        """Display result for a single algorithm in its tab"""
        text_widget = self.result_texts[algorithm]
        text_widget.delete(1.0, tk.END)
        
        if goal_state is None:
            text_widget.insert(tk.END, f"{algorithm}\n{'='*35}\n")
            text_widget.insert(tk.END, "❌ NO SOLUTION FOUND!\n")
            text_widget.insert(tk.END, f"\nNodes expanded: {nodes_expanded}\n")
            text_widget.insert(tk.END, f"Time: {runtime:.4f} seconds\n")
            return
        
        # Store solution path for this algorithm
        path, moves = reconstruct_path(goal_state)
        
        text_widget.insert(tk.END, f"{algorithm}\n{'='*35}\n")
        text_widget.insert(tk.END, f"✅ SOLUTION FOUND!\n\n")
        text_widget.insert(tk.END, f"Steps to goal: {len(moves)}\n")
        text_widget.insert(tk.END, f"Moves: {' → '.join(moves)}\n\n")
        text_widget.insert(tk.END, f"Nodes expanded: {nodes_expanded}\n")
        text_widget.insert(tk.END, f"Time: {runtime:.4f} seconds\n")
        if max_frontier > 0:
            text_widget.insert(tk.END, f"Max frontier size: {max_frontier}\n")
        text_widget.insert(tk.END, f"Search depth: {goal_state.depth}\n")
        
        # Show the path steps
        text_widget.insert(tk.END, f"\n{'='*35}\n")
        text_widget.insert(tk.END, "SOLUTION STEPS:\n")
        text_widget.insert(tk.END, f"{'='*35}\n")
        
        for i, state in enumerate(path):
            text_widget.insert(tk.END, f"\nStep {i}:\n")
            if state.move:
                text_widget.insert(tk.END, f"Move: {state.move}\n")
            # Display board as grid
            for row in range(3):
                row_str = "  "
                for col in range(3):
                    val = state.board[row*3 + col]
                    row_str += f"{val if val != 0 else ' '}  "
                text_widget.insert(tk.END, row_str + "\n")
        
        # If this is the currently selected algorithm in notebook, enable animation
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        if current_tab == algorithm:
            self.solution_path = path
            self.current_step = 0
            self.prev_btn.config(state='normal')
            self.next_btn.config(state='normal')
            self.animate_btn.config(state='normal')
            if self.solution_path:
                self.current_state = self.solution_path[0]
                self.update_display()
    
    def run_all_algorithms(self):
        """Run all algorithms and display results"""
        if not self.current_state:
            messagebox.showwarning("Warning", "Please generate a puzzle first!")
            return
        
        self.status_bar.config(text="Running all algorithms... This may take a moment")
        self.root.update()
        
        algorithms = ["BFS", "DFS", "IDDFS", "A* Manhattan", "A* Euclidean"]
        
        for algo in algorithms:
            self.run_single_algorithm(algo)
            self.root.update()
        
        self.status_bar.config(text="All algorithms completed!")
        messagebox.showinfo("Complete", "All algorithms have finished running!\nCheck each tab for results.")
        
    def next_step(self):
        """Show next step in solution"""
        if self.current_step + 1 < len(self.solution_path):
            self.current_step += 1
            self.current_state = self.solution_path[self.current_step]
            self.update_display()
            self.status_bar.config(text=f"Step {self.current_step} of {len(self.solution_path)-1}")
            
    def prev_step(self):
        """Show previous step in solution"""
        if self.current_step > 0:
            self.current_step -= 1
            self.current_state = self.solution_path[self.current_step]
            self.update_display()
            self.status_bar.config(text=f"Step {self.current_step} of {len(self.solution_path)-1}")
            
    def animate_solution(self):
        """Animate the solution"""
        if not self.solution_path or self.animation_id:
            return
            
        self.animate_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.run_all_btn.config(state='disabled')
        self.random_btn.config(state='disabled')
        
        def animate_step(step=1):
            if step >= len(self.solution_path):
                self.stop_animation()
                return True
            
            self.current_state = self.solution_path[step]
            self.update_display()
            self.current_step = step
            self.status_bar.config(text=f"Animating step {step} of {len(self.solution_path)-1}")
            
            self.animation_id = self.root.after(500, animate_step, step + 1)
            return True
        
        animate_step()
        
    def stop_animation(self):
        """Stop the animation"""
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
            
        self.animate_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.run_all_btn.config(state='normal')
        self.random_btn.config(state='normal')
        self.status_bar.config(text="Animation stopped")


# ------------------------- Main -------------------------
def main():
    # Run terminal tests FIRST (for the fixed initial state)
    run_terminal_tests()
    
    # Then launch GUI
    root = tk.Tk()
    gui = PuzzleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()