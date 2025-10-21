# Example Workflows

This directory contains ready-to-use example workflows for ComfyUI Qwen3-VL integration.

## 📚 Workflow Categories

### Local Inference Workflows (Qwen3VLProcessor)
Traditional workflows using local model inference.

### API-Based Workflows (Qwen3VLAPINode / Qwen3VLAPIAdvanced)
Modern workflows using DashScope API for cloud-based inference.

---

## Available Examples

### 1. Text-Only Query (`examples_workflow_text_only.json`)

**Purpose**: Simple text-only inference without any images or videos.

**Use Cases**:
- General Q&A
- Text generation
- Information retrieval
- Testing basic functionality

**Workflow**:
```
Text Prompt → Qwen3-VL Processor → Display Response
```

**Example Prompts**:
- "What is artificial intelligence?"
- "Explain quantum computing in simple terms"
- "Write a poem about nature"

---

### 2. Single Image Analysis (`examples_workflow_single_image.json`)

**Purpose**: Analyze a single image with text prompts.

**Use Cases**:
- Image description
- Object detection
- Scene understanding
- Text extraction (OCR)
- Image classification

**Workflow**:
```
Load Image → Qwen3-VL Processor → Display Response
```

**Example Prompts**:
- "Describe this image in detail"
- "What objects are in this image?"
- "Extract all text from this image"
- "What is the main subject of this image?"

---

### 3. Multi-Image Comparison (`examples_workflow_multi_image.json`)

**Purpose**: Compare and analyze multiple images together.

**Use Cases**:
- Image comparison
- Relationship analysis
- Batch processing
- Similarity detection
- Difference identification

**Workflow**:
```
Load Image 1 ─┐
Load Image 2 ─┼→ Combine Images → Qwen3-VL Processor → Display Response
Load Image 3 ─┘
```

**Example Prompts**:
- "Compare these images and identify similarities"
- "What are the differences between these images?"
- "Describe the relationship between these images"
- "Which image is most similar to the first one?"

**Note**: You can combine up to 5 images using the "Combine Images for Qwen3-VL" node.

---

### 4. Video Summarization (`examples_workflow_video.json`)

**Purpose**: Analyze and summarize video content.

**Use Cases**:
- Video summarization
- Video understanding
- Scene analysis
- Action recognition
- Event detection

**Workflow**:
```
Load Video → Qwen3-VL Processor → Display Response
```

**Example Prompts**:
- "Summarize this video"
- "What is happening in this video?"
- "Describe the main events in this video"
- "What are the key scenes in this video?"

**Video Parameters**:
- **FPS**: Frames per second to sample (default: 2)
- **Max Frames**: Maximum number of frames to process (default: 128)

---

## How to Use These Examples

### Step 1: Load a Workflow
1. Open ComfyUI
2. Click **"Load"** button
3. Navigate to `custom_nodes/ComfyUI_Qwen3-VL/examples/`
4. Select one of the JSON files

### Step 2: Configure the Workflow
1. **Select Model**: Choose a Qwen3-VL model (e.g., Qwen3-VL-4B-Instruct)
2. **Set Text Prompt**: Enter your query or description
3. **Adjust Parameters** (optional):
   - Temperature: 0.7 (balanced)
   - Top-p: 0.8 (diverse)
   - Max Tokens: 2048 (output length)

### Step 3: Run the Workflow
1. Click **"Queue Prompt"** or press **Ctrl+Enter**
2. Wait for the model to process
3. View the response in the Display node

---

## Model Selection Guide

| Model | Speed | Quality | Memory | Best For |
|-------|-------|---------|--------|----------|
| 4B-Instruct | ⚡⚡⚡ | ⭐⭐⭐ | 8GB | Fast inference |
| 4B-Thinking | ⚡⚡ | ⭐⭐⭐⭐ | 8GB | Reasoning |
| 8B-Instruct | ⚡⚡ | ⭐⭐⭐⭐ | 16GB | Balanced |
| 8B-Thinking | ⚡ | ⭐⭐⭐⭐⭐ | 16GB | Complex tasks |
| 4B-Instruct-FP8 | ⚡⚡⚡ | ⭐⭐⭐ | 4GB | Limited VRAM |

---

## Tips for Best Results

### For Faster Processing
- Use 4B models instead of 8B
- Lower max_pixels value
- Reduce max_new_tokens
- Enable flash_attention_2 if supported

### For Better Quality
- Use 8B or larger models
- Use Thinking variants for complex tasks
- Increase max_new_tokens
- Use higher max_pixels for detail

### For Limited Memory
- Use FP8 quantized models
- Enable 4-bit or 8-bit quantization
- Use 4B models
- Reduce max_pixels

---

## Troubleshooting

### Model Not Found
- Ensure internet connection is active
- Check Hugging Face access
- Models will auto-download on first use

### Out of Memory (OOM)
- Use smaller models (4B)
- Enable quantization
- Reduce max_pixels
- Lower max_new_tokens

### Slow Processing
- Enable flash_attention_2
- Use 4B models
- Reduce video FPS
- Lower max_new_tokens

---

## Creating Custom Workflows

You can create your own workflows by:
1. Modifying these examples
2. Combining different nodes
3. Adding multiple processing steps
4. Saving as JSON

For more information, see the main [README.md](../README.md) and [ADVANCED_FEATURES.md](../ADVANCED_FEATURES.md).

---

---

## 🌐 API-Based Workflows (NEW!)

### Available API Workflows

1. **api_workflow_single_image.json** - Single image analysis via API
2. **api_workflow_multi_image.json** - Multi-image comparison via API
3. **api_workflow_video.json** - Video analysis via API
4. **api_workflow_streaming.json** - Streaming output via API
5. **api_workflow_thinking_mode.json** - Thinking mode analysis via API
6. **api_workflow_text_only.json** - Text-only queries via API
7. **api_workflow_advanced_mixed.json** - Image + Video analysis via API

### Key Advantages of API Workflows

✅ **No Local Model Required** - Use cloud-based inference
✅ **Scalable** - Handle multiple requests efficiently
✅ **Cost-Effective** - Pay only for what you use
✅ **Always Updated** - Latest model versions automatically
✅ **Streaming Support** - Real-time response streaming
✅ **Advanced Features** - Thinking mode, multi-image support

### Quick Start with API Workflows

1. Get API Key from [Aliyun Bailian](https://bailian.aliyun.com/)
2. Load one of the `api_workflow_*.json` files
3. Set your API Key in the node
4. Run the workflow

### API Workflow Documentation

For detailed information about API workflows, see:
- [API_WORKFLOWS_GUIDE.md](./API_WORKFLOWS_GUIDE.md) - Complete guide
- [API_NODE_GUIDE.md](../API_NODE_GUIDE.md) - Usage guide
- [API_REFERENCE.md](../API_REFERENCE.md) - API reference

---

## Support

For issues or questions:
1. Check [QUICK_REFERENCE.md](../QUICK_REFERENCE.md)
2. Review [ADVANCED_FEATURES.md](../ADVANCED_FEATURES.md)
3. Check [TESTING.md](../TESTING.md)
4. See [API_WORKFLOWS_GUIDE.md](./API_WORKFLOWS_GUIDE.md) for API workflows
5. Open an issue on GitHub

---

**Happy inferencing! 🚀**

