# Qwen3-VL API 工作流示例指南

本指南介绍如何使用 Qwen3-VL API 节点创建各种工作流。

---

## 📋 可用的工作流示例

### 1. 单图像分析 (`api_workflow_single_image.json`)

**功能**: 分析单张图像

**工作流结构**:
```
Load Image → Qwen3-VL API → Display Output
```

**使用场景**:
- 图像描述
- 物体检测
- 场景理解
- 文本提取 (OCR)
- 图像分类

**示例提示词**:
```
"Describe this image in detail. What do you see? Include colors, objects, and composition."
```

**关键参数**:
- `model_name`: qwen3-vl-235b-a22b-instruct
- `max_tokens`: 1024
- `temperature`: 0.7
- `stream`: false

---

### 2. 多图像比较 (`api_workflow_multi_image.json`)

**功能**: 比较和分析多张图像

**工作流结构**:
```
Load Image 1 ─┐
Load Image 2 ─┼→ Qwen3-VL API Advanced → Display Output
Load Image 3 ─┘
```

**使用场景**:
- 图像比较
- 相似性检测
- 差异识别
- 关系分析
- 批量处理

**示例提示词**:
```
"Compare these three images. What are the similarities and differences? 
Describe each image and then provide a comprehensive comparison."
```

**关键参数**:
- `model_name`: qwen3-vl-235b-a22b-instruct
- `max_tokens`: 2048
- `image_1`, `image_2`, `image_3`: 图像输入
- `top_k`: 20
- `repetition_penalty`: 1.0

**支持的图像数量**: 最多 4 张

---

### 3. 视频分析 (`api_workflow_video.json`)

**功能**: 分析和总结视频内容

**工作流结构**:
```
Video Input → Qwen3-VL API → Display Output
```

**使用场景**:
- 视频总结
- 视频理解
- 场景分析
- 动作识别
- 事件检测

**示例提示词**:
```
"Analyze this video. What is happening? Describe the main events, 
objects, and actions. Provide a comprehensive summary."
```

**关键参数**:
- `model_name`: qwen3-vl-235b-a22b-instruct
- `max_tokens`: 2048
- `video`: 视频文件路径或 URL

**支持的视频格式**:
- MP4, WebM, MOV
- 本地路径: `/path/to/video.mp4`
- URL: `https://example.com/video.mp4`
- Base64: `data:video/mp4;base64,...`

---

### 4. 流式输出 (`api_workflow_streaming.json`)

**功能**: 使用流式输出实时获取响应

**工作流结构**:
```
Load Image → Qwen3-VL API (stream=true) → Display Output
```

**使用场景**:
- 长文本生成
- 实时响应
- 交互式应用
- 大量输出处理

**示例提示词**:
```
"Provide a detailed analysis of this image. Include:
1. Main subject and composition
2. Colors and lighting
3. Objects and their relationships
4. Possible context or story
5. Artistic or technical observations"
```

**关键参数**:
- `stream`: true
- `max_tokens`: 2048
- `temperature`: 0.8

**优势**:
- 实时获取输出
- 不需要等待完整响应
- 更好的用户体验

---

### 5. 思考模式 (`api_workflow_thinking_mode.json`)

**功能**: 使用思考模式进行深度推理

**工作流结构**:
```
Load Image → Qwen3-VL API Advanced (thinking=true) → Display Output
```

**使用场景**:
- 复杂分析
- 深度推理
- 困难问题解决
- 详细解释

**示例提示词**:
```
"This image contains complex visual elements. Please analyze it deeply:
1. What is the primary subject?
2. What are the secondary elements?
3. How do they relate to each other?
4. What might be the purpose or context?
5. What insights can you derive from the composition?"
```

**关键参数**:
- `model_name`: qwen3-vl-235b-a22b-thinking
- `enable_thinking`: true
- `max_tokens`: 4096
- `temperature`: 0.5

**优势**:
- 更深入的推理
- 更详细的分析
- 更准确的结果

---

### 6. 文本只查询 (`api_workflow_text_only.json`)

**功能**: 纯文本查询，不需要图像或视频

**工作流结构**:
```
Text Prompt → Qwen3-VL API → Display Output
```

**使用场景**:
- 一般问答
- 文本生成
- 信息检索
- 功能测试

**示例提示词**:
```
"Explain the concept of machine learning in simple terms. Include:
1. What is machine learning?
2. How does it work?
3. What are common applications?
4. What are the limitations?
5. What is the future of machine learning?"
```

**关键参数**:
- `model_name`: qwen3-vl-235b-a22b-instruct
- `max_tokens`: 2048
- 无需图像或视频输入

---

### 7. 高级混合分析 (`api_workflow_advanced_mixed.json`)

**功能**: 同时分析图像和视频

**工作流结构**:
```
Load Image ─┐
            ├→ Qwen3-VL API Advanced → Display Output
Video Input ─┘
```

**使用场景**:
- 图像与视频对比
- 参考图像分析
- 多模态理解
- 复杂场景分析

**示例提示词**:
```
"Analyze this reference image and the video:
1. Describe the reference image in detail
2. Summarize the video content
3. Compare the reference image with the video content
4. Identify any relationships or connections
5. Provide insights on how they relate to each other"
```

**关键参数**:
- `model_name`: qwen3-vl-235b-a22b-instruct
- `max_tokens`: 3000
- `image_1`: 参考图像
- `video_path`: 视频文件

---

## 🚀 如何使用这些工作流

### 步骤 1: 加载工作流

1. 打开 ComfyUI
2. 点击 **"Load"** 按钮
3. 导航到 `custom_nodes/ComfyUI_Qwen3-VL/examples/`
4. 选择一个 JSON 文件

### 步骤 2: 配置工作流

1. **设置 API Key**
   - 在节点中输入你的 DashScope API Key
   - 或设置环境变量: `DASHSCOPE_API_KEY`

2. **选择模型**
   - `qwen3-vl-235b-a22b-instruct` - 标准模型（推荐）
   - `qwen3-vl-235b-a22b-thinking` - 思考模式
   - `qwen-vl-max` - 最大性能
   - `qwen-vl-plus` - 平衡模型

3. **调整参数**
   - `temperature`: 0.7（平衡）
   - `top_p`: 0.8（多样性）
   - `max_tokens`: 1024-4096（输出长度）

### 步骤 3: 运行工作流

1. 点击 **"Queue Prompt"** 或按 **Ctrl+Enter**
2. 等待模型处理
3. 在 Display 节点中查看响应

---

## 📊 模型选择指南

| 模型 | 速度 | 质量 | 成本 | 最佳用途 |
|------|------|------|------|---------|
| qwen3-vl-235b-a22b-instruct | ⚡⚡ | ⭐⭐⭐⭐ | 中等 | 通用任务 |
| qwen3-vl-235b-a22b-thinking | ⚡ | ⭐⭐⭐⭐⭐ | 高 | 复杂推理 |
| qwen-vl-max | ⚡ | ⭐⭐⭐⭐⭐ | 高 | 最高质量 |
| qwen-vl-plus | ⚡⚡⚡ | ⭐⭐⭐ | 低 | 快速响应 |

---

## 💡 最佳实践

### 获得更快的处理速度

- 使用 `qwen-vl-plus` 模型
- 降低 `max_tokens` 值
- 禁用 `stream` 模式
- 使用较小的图像分辨率

### 获得更好的质量

- 使用 `qwen3-vl-235b-a22b-instruct` 或更大的模型
- 对复杂任务使用思考模式
- 增加 `max_tokens`
- 使用更详细的提示词

### 降低成本

- 使用 `qwen-vl-plus` 模型
- 减少输入令牌数
- 减少输出令牌数
- 批量处理请求

---

## 🔧 自定义工作流

你可以通过以下方式创建自己的工作流：

1. **修改现有示例**
   - 复制一个 JSON 文件
   - 修改参数和提示词
   - 保存为新文件

2. **组合不同节点**
   - 添加多个 API 节点
   - 连接不同的输入
   - 创建复杂的处理流程

3. **添加处理步骤**
   - 在 API 调用前处理图像
   - 在输出后处理文本
   - 添加条件逻辑

---

## 📝 工作流 JSON 结构

基本结构：

```json
{
  "1": {
    "inputs": {
      "image": "example.jpg"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "2": {
    "inputs": {
      "text_prompt": "Your prompt here",
      "api_key": "your_api_key",
      "model_name": "qwen3-vl-235b-a22b-instruct",
      "max_tokens": 1024,
      "temperature": 0.7,
      "top_p": 0.8,
      "image": ["1", 0],
      "stream": false
    },
    "class_type": "Qwen3VLAPINode",
    "_meta": {
      "title": "Qwen3-VL API"
    }
  }
}
```

---

## ❓ 常见问题

**Q: 如何获取 API Key？**
A: 访问 https://bailian.aliyun.com/ 注册并创建 API Key。

**Q: 支持哪些图像格式？**
A: JPEG、PNG、WebP、GIF 等常见格式。

**Q: 支持哪些视频格式？**
A: MP4、WebM、MOV 等常见格式。

**Q: 如何处理大文件？**
A: 使用流式输出或分割文件进行多次请求。

**Q: 是否支持离线使用？**
A: 不支持，需要网络连接到 DashScope API。

---

## 🎓 更多资源

- [API_NODE_GUIDE.md](../API_NODE_GUIDE.md) - 完整使用指南
- [API_REFERENCE.md](../API_REFERENCE.md) - API 参考文档
- [README.md](../README.md) - 项目主文档

---

**祝你使用愉快！🚀**

