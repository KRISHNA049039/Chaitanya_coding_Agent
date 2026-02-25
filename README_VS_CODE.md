Running Kiro in VS Code

Tasks

- Run the integrated task to start the CLI chat in the integrated terminal:

```bash
# From the workspace root in VS Code, run the task:
# Terminal → Run Task → "Run Kiro Chat"
python -u cli.py chat
```

VS Code Extension (development)

1. Open the workspace in VS Code.
2. Open the `kiro-vscode-extension` folder in the Explorer.
3. Press `F5` to launch the Extension Development Host.
4. In the Extension Development Host, open the Command Palette and run `Kiro: Start Chat`.

Benchmarks

Run the microbenchmarks to compare methods:

```bash
python -m benchmarks.bench_strings
```

String utilities

- `string_utils.py` contains helpers: `StringBuilder`, `fast_replace`, `safe_split`, `join_parts`, `use_stringio_write`, and `merge_lists_with_indices` (avoid `pop(0)`).
