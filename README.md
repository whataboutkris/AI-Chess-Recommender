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

#### Option A: Ubuntu/Debian (Recommended)

```bash
sudo apt-get update
sudo apt-get install -y stockfish
```

#### Option A1: Windows (Recommended)

```bash
pip3 install stockfish 
```

#### Option B: Fedora/RHEL

```bash
sudo dnf install -y stockfish
```

#### Option C: Arch Linux

```bash
sudo pacman -S stockfish
```

#### Option D: macOS (Homebrew)

```bash
brew install stockfish
```

#### Option E: Manual Installation (All Platforms)

1. Download Stockfish from [https://stockfishchess.org/download/](https://stockfishchess.org/download/)
2. Extract the binary to a location in your PATH or a known directory
3. Make it executable (Linux/macOS):
   ```bash
   chmod +x /path/to/stockfish
   ```

### 3. Verify Stockfish Installation

Check that stockfish is accessible:

```bash
stockfish --version
```

---

## Setup Virtual Environment (Optional but Recommended)

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install python-chess:

```bash
pip install python-chess
```

---

## Troubleshooting

### Stockfish Not Found

If you get a "stockfish not found" error when running the application:

1. Ensure stockfish is installed: `which stockfish`
2. If installed in a non-standard location, update the path in your code
3. Specify the full path to the stockfish binary when initializing the engine

### Python-Chess Import Error

If you get an ImportError for chess:

```bash
pip3 install --upgrade python-chess
```

---

## Next Steps

Once installed, you can run the Chess Recommender System:

```bash
python3 main.py
```
