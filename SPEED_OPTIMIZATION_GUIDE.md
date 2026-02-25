# ⚡ Speed Optimization Guide

## Quick Wins

### 1. Use Smaller Models
```cmd
# Fastest (2B parameters)
ollama pull gemma2:2b

# Fast (3B parameters)
ollama pull llama3.2:3b
ollama pull qwen2.5:3b

# Balanced (7B parameters)
ollama pull mistral:7b
```

Update `.env`:
```env
LLM_MODEL_NAME=gemma2:2b
LLM_MAX_TOKENS=1024
LLM_TIMEOUT=60
```

### 2. Enable GPU Acceleration

Check GPU:
```cmd
ollama ps
```

If it shows "100% CPU", enable GPU:

**For Intel Arc GPU (you have this):**
```cmd
# Set environment variable
set OLLAMA_INTEL_GPU=1
ollama serve
```

**For NVIDIA:**
```cmd
# Should work automatically
nvidia-smi
```

### 3. Reduce Context Window

In `.env`:
```env
LLM_MAX_TOKENS=1024  # Instead of 2048
```

### 4. Optimize System Prompt

Shorter prompts = faster responses. The agent already does this.

### 5. Use Quantized Models

```cmd
# Q4 quantization (faster, slightly less accurate)
ollama pull llama3.2:3b-q4_0

# Q8 quantization (balanced)
ollama pull llama3.2:3b-q8_0
```

## Speed Comparison

| Model | Size | Speed (tokens/s) | Quality |
|-------|------|------------------|---------|
| gemma2:2b | 1.6GB | ~15 tok/s | Good |
| llama3.2:3b | 2.0GB | ~10 tok/s | Better |
| mistral:7b | 4.1GB | ~5 tok/s | Best |
| llama3.1:8b | 4.9GB | ~3 tok/s | Best |

*On CPU. GPU is 5-10x faster!*

## Recommended Setup

For your Intel Arc GPU:
```env
LLM_MODEL_NAME=llama3.2:3b
LLM_MAX_TOKENS=1024
LLM_TIMEOUT=120
```

Then:
```cmd
set OLLAMA_INTEL_GPU=1
ollama serve
```

Expected speed: 20-30 tokens/second (vs 3-5 on CPU)

## Advanced: Parallel Requests

For multiple users, use async:
```python
# Already implemented in web_ui.py
```

## Monitoring

Check performance:
```cmd
ollama ps
```

Look for:
- GPU usage (should be >0%)
- Memory usage
- Token generation rate
