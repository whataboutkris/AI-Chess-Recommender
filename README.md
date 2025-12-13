# AI Chess Recommender System
This project aims to develop an AI Chess Move Recommender that analyzes a given board position and suggests optimal moves using adversarial search. The system focuses on fast, explainable recommendations suitable for players seeking strategic guidance. The model will evaluate future positions through a custom heuristic and provide ranked move suggestions.

## Installation Guide

This guide explains how to install the required dependencies:

- **python-chess** (Python library for chess board logic)
- **Stockfish** (UCI chess engine used for evaluation and recommendations)

Works on Ubuntu, Debian, Pop!_OS, Linux Mint, and most other Linux distributions.

---

## Prerequisites

Ensure Python 3.7+ and pip are installed:
If not found, install Python (windows) here: https://www.python.org/downloads/
Commands below to check:
```bash
python3 --version
pip3 --version
```

---

## Installation Steps

### 1. Install python-chess

Install the python-chess library via pip:

```bash
pip3 install python-chess
```

Verify the installation:

```bash
python3 -c "import chess; print('python-chess installed successfully')"
```

### 2. Install Stockfish
Install stockfish and extract the files to the empty stockfish folder in the repository. 
### NOTE: **MAKE SURE YOU RENAME YOUR STOCKFISH EXECUTABLE TO "stockfish.exe"**

Install Stockfish from the website below:
https://stockfishchess.org/download/

Additionally, you need to install the stockfish library: 
#### Option A: Windows (Recommended)
```bash
pip3 install stockfish 
```


### NOTE: **MAKE SURE YOU RENAME YOUR stockfish-windows-x86-64-avx2.exe TO "stockfish.exe"**



#### Option B: Manual Installation (All Platforms)

1. Download Stockfish from [https://stockfishchess.org/download/](https://stockfishchess.org/download/)
2. Extract the binary to a location in your PATH or a known directory
3. Make it executable (Linux/macOS):
   ```bash
   chmod +x /path/to/stockfish
   ```

Your Stockfish directory should look like this:
<img width="660" height="301" alt="image" src="https://github.com/user-attachments/assets/3ad129ef-641c-4735-a45a-fd813b6ad119" />

### 3. Verify Stockfish Installation

Check that stockfish is accessible:

```bash
stockfish 
```
### (WINDOWS OS) If stockfish doesn't show up in your terminal, you need to include stockfish into your windows path!
<img width="616" height="581" alt="image" src="https://github.com/user-attachments/assets/fea142aa-7520-424a-b1d1-e89c2342762b" />

### 4. Install Rich

```bash
pip install rich
```

### 5. Install numpy 
```
pip install numpy
```

---

## Troubleshooting

### Stockfish Not Found

If you get a "stockfish not found" error when running the application:

1. Ensure stockfish is actually installed!
2. If installed in a non-standard location, update the path in your code
3. Specify the full path to the stockfish binary when initializing the engine (found at the top of /tests/test_scenarios and in line 86 in /cli/recommender.py )

Additionally: If you installed Stockfish on a CLI, you need to restart the CLI for changes to take effect. 


## Next Steps

Once installed, you can run the Chess Recommender System:

```bash
python3 main.py
```

If you'd like to mess around with max_node value or just this project in general, you can run tests.
```bash
python -m tests.test_scenarios
```

If you are not familiar with chess notation, this guide will help:
https://www.chess.com/terms/chess-notation
