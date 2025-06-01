#!/bin/bash

set -e  # Exit on error

# Check if poetry is available
if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Add Poetry to PATH for the current session
    export PATH="$HOME/.local/bin:$PATH"
    
    # Optionally persist to shell config (optional)
    SHELL_CONFIG="$HOME/.bashrc"
    if [[ $SHELL == *"zsh" ]]; then
        SHELL_CONFIG="$HOME/.zshrc"
    fi
    if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_CONFIG"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
        echo ">> Added poetry to PATH in $SHELL_CONFIG"
    fi
fi

echo "✅ Poetry is available. Installing dependencies..."
poetry install

