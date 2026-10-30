# 5022CMD Advanced Algorithms – Portfolio

**Student:** Chloe Yeoh Wen Ci | **Student ID:** P24016574 | **CU ID:** 17955177 | **Module Leader:** Vimala Doraisamy

## Requirements
- Python 3.12+ (tested on Python 3.12.10, macOS)
- No external libraries (standard library only)

## Q1 – Hashing (Pharmacy Inventory System)
Hash table using open addressing with linear probing.
```
cd Q1_Hashing
python3 inventory_system.py     # inventory menu
python3 performance_test.py     # hash table vs array experiment
```
**Features:** insert, search, edit, delete (tombstones), view all products with low-stock status, hash table view showing collisions and probe paths, input validation.
Experiment results: `Q1_results.txt`

## Q2 – Graph (Course Prerequisite System)
Unweighted directed graph; edge Y → X means "Y is a prerequisite of X".
```
cd Q2_Graph
python3 course_system.py
```
**Features:** view all courses, course details, prerequisites (incoming edges), courses unlocked (outgoing edges), add a course, core/elective profile visibility, add and remove prerequisites, circular prerequisite prevention (BFS), prerequisite map.

## Q3 – Concurrency (Fibonacci Multithreading)
Compares Fibonacci(35, 38, 40) with and without threads over 10 rounds.
```
cd Q3_Concurrency
python3 fibonacci.py              # call-count table supporting the Big-O analysis
python3 threading_experiment.py   # with vs without multithreading
```
> Note: the full experiment takes about 5 minutes.

Experiment results: `Q3_results.txt`

## AI Tool Acknowledgement
**Claude** was used throughout this assignment to explain concepts, suggest the project structure and review code, and help design the command-line output. I tested every feature, correct the code, requested and made changes (for example adding spacing, and fixing table alignment), ran all experiments, and analysed the results myself.
