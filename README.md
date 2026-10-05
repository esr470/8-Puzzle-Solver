# 🧩 8-Puzzle Solver

> 🤖 **AI-based 8-Puzzle Solver** implemented in Python using different search algorithms and a graphical user interface.

---

## 📌 Project Description

This project solves the classic **8-Puzzle problem** using several Artificial Intelligence search algorithms.

The puzzle consists of a **3×3 board** containing numbers from 1 to 8 and one empty space.

🎯 The goal is to reach the target state:

```text
┌───┬───┬───┐
│ 0 │ 1 │ 2 │
├───┼───┼───┤
│ 3 │ 4 │ 5 │
├───┼───┼───┤
│ 6 │ 7 │ 8 │
└───┴───┴───┘
```

The program checks whether a puzzle is solvable, finds a solution, displays the solution steps, and compares the performance of different search algorithms.

---

## 🔎 Search Algorithms

The project implements:

| 🔹 Algorithm       | 📝 Description                         |
| ------------------ | -------------------------------------- |
| 🌳 **BFS**         | Breadth-First Search                   |
| 🔍 **DFS**         | Depth-First Search                     |
| 🔄 **IDDFS**       | Iterative Deepening Depth-First Search |
| ⭐ **A* Manhattan** | A* using Manhattan Distance            |
| ⭐ **A* Euclidean** | A* using Euclidean Distance            |

---

## 🧠 Heuristics

### 📏 Manhattan Distance

Calculates the total horizontal and vertical distance of each tile from its goal position.

### 📐 Euclidean Distance

Calculates the straight-line distance between each tile and its goal position.

---

## ✨ Features

* 🎲 Generate random solvable puzzles
* ✅ Check puzzle solvability
* ▶️ Run individual search algorithms
* 🚀 Run all algorithms
* 📋 Display solution steps
* 🔢 Display number of steps
* 🔍 Display nodes expanded
* ⏱️ Display running time
* 📊 Display maximum frontier size
* ⚖️ Compare algorithm results
* 🎬 Animate the solution step by step
* ◀️ Previous and Next controls for solution steps
* 🖥️ Graphical User Interface using Tkinter
* 💻 Terminal output for algorithm testing

---

## 🛠️ Technologies Used

```text
🐍 Python
🖼️ Tkinter
🌳 Breadth-First Search
🔎 Depth-First Search
🔄 Iterative Deepening DFS
⭐ A* Search
📏 Manhattan Heuristic
📐 Euclidean Heuristic
```

---

## 📦 Requirements

**Python 3.x**

The project uses Python standard libraries, including:

```text
tkinter
heapq
math
time
random
collections
copy
```

---

## ▶️ How to Run

### 1️⃣ Clone the repository

```bash
git clone https://github.com/esr470/8-Puzzle-Solver.git
```

### 2️⃣ Go to the project folder

```bash
cd 8-Puzzle-Solver
```

### 3️⃣ Run the program

```bash
python 8_puzzle4.py
```

---

## ⚙️ How It Works

When the program starts, it first runs the algorithms on a fixed puzzle state and displays the results in the terminal.

After that, the graphical interface opens.

From the GUI, you can:

1. 🎲 Generate a random solvable puzzle.
2. ▶️ Run one algorithm.
3. 🚀 Run all algorithms.
4. 📋 View the solution path.
5. ◀️▶️ Move through the solution using Previous and Next.
6. 🎬 Animate the solution.

---

## 📂 Project Structure

```text
8-Puzzle-Solver/
│
├── 🐍 8_puzzle4.py
└── 📖 README.md
```

---

## 🎯 Goal

The main goal of this project is to demonstrate and compare different AI search algorithms for solving the **8-Puzzle problem**.

---

## 👩‍💻 Project

**8-Puzzle Solver — AI Search Algorithms**

⭐ If you find this project useful, feel free to explore the code and experiment with the different algorithms!
