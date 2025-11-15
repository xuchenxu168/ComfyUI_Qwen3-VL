# ComfyUI Qwen3-VL Integration

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)
![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-orange.svg)

**强大的 Qwen3-VL 视觉语言模型 ComfyUI 集成插件**

支持本地模型推理 + 云端 API 调用 | 图像分析 | 视频理解 | 多模态对话

[English](#english-version) | [中文文档](#中文文档)

</div>

---

## 📑 目录

- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [API 申请指南](#-api-申请指南)
- [节点说明](#-节点说明)
- [配置说明](#-配置说明)
- [使用示例](#-使用示例)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)
- [联系支持](#-联系支持)

---

## ✨ 功能特性

### 🎯 核心功能

- **🔌 双模式支持**
  - 本地模型推理（支持 4B/8B 模型，FP8/4bit/8bit 量化）
  - 云端 API 调用（通义万像、Comfly、T8、硅基流动等多个服务商）

- **🖼️ 多模态输入**
  - 单图/多图分析（最多 4 张图片）
  - 视频理解（支持多种格式）
  - 纯文本对话
  - 图文混合输入

- **⚡ 高级特性**
  - 流式输出（实时响应）
  - 思维链模式（Thinking Mode）
  - 自动图像压缩（最大边长 2048px）
  - 代理支持（HTTP/SOCKS5）
  - 自动重试机制

- **🎨 ComfyUI 原生集成**
  - 直接接受 IMAGE/VIDEO 张量
  - 无需中间转换节点
  - 完整的工作流示例

---

## 🚀 快速开始

### 安装步骤

1. **克隆仓库到 ComfyUI 自定义节点目录**
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/yourusername/ComfyUI_Qwen3-VL.git
```

2. **安装依赖**
```bash
cd ComfyUI_Qwen3-VL
pip install -r requirements.txt
```

3. **配置 API（可选）**
   - 编辑 `Qwen3-VL-config.json`
   - 填入你的 API Key（见下方 [API 申请指南](#-api-申请指南)）

4. **重启 ComfyUI**

### 系统要求

| 组件 | 最低要求 | 推荐配置 |
|------|---------|---------|
| **GPU** | NVIDIA GPU 8GB VRAM | RTX 3090/4090 24GB+ |
| **内存** | 16GB RAM | 32GB+ RAM |
| **存储** | 20GB 可用空间 | 100GB+ SSD |
| **Python** | 3.10+ | 3.11 |
| **CUDA** | 11.8+ | 12.1+ |

> **注意**：
> - 本地模型推理需要较高配置
> - API 模式只需基本配置即可运行

---

## 🔑 API 申请指南

### 1️⃣ 通义万像 API（阿里云）

**官方网站**: https://dashscope.aliyun.com/

**申请步骤**:
1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 登录/注册阿里云账号
3. 进入 API-KEY 管理页面
4. 点击"创建新的 API-KEY"
5. 复制生成的 API Key（格式：`sk-xxxxxx`）

**免费额度**:
- 新用户赠送 100 万 tokens
- 每月免费额度：500 万 tokens

**支持模型**:
- `qwen3-vl-235b-a22b-instruct` - 指令微调版本
- `qwen3-vl-235b-a22b-thinking` - 思维链版本
- `qwen-vl-max` - 最大能力版本
- `qwen-vl-plus` - 平衡版本

**配置示例**:
```json
{
  "api": {
    "providers": {
      "通义万像API": {
        "name": "dashscope",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key": "sk-你的API密钥"
      }
    }
  }
}
```

---

### 2️⃣ Comfly API

**官方网站**: https://ai.comfly.chat/

**申请步骤**:
1. 访问 [Comfly AI 平台](https://ai.comfly.chat/)
2. 注册账号并登录
3. 进入"API 管理"页面
4. 创建新的 API Key
5. 复制生成的密钥（格式：`sk-xxxxxx`）

**定价**:
- 按 token 计费
- 支持充值使用

**支持模型**:
- `qwen3-vl-235b-a22b` - Qwen3-VL 235B 模型

**配置示例**:
```json
{
  "api": {
    "providers": {
      "Comfly API": {
        "name": "Comfly",
        "base_url": "https://ai.comfly.chat/v1",
        "api_key": "sk-你的API密钥",
        "max_images": 4
      }
    }
  }
}
```

---

### 3️⃣ T8 贞贞 AI 工坊

**官方网站**: https://ai.t8star.cn/

**申请步骤**:
1. 访问 [T8 AI 工坊](https://ai.t8star.cn/)
2. 注册并登录账号
3. 进入 API 管理界面
4. 生成 API Key
5. 复制密钥

**特点**:
- 支持多种 AI 模型
- 稳定的服务质量

**支持模型**:
- `qwen3-vl-235b-a22b` - Qwen3-VL 235B 模型

**配置示例**:
```json
{
  "api": {
    "providers": {
      "t8的贞贞AI工坊": {
        "name": "T8",
        "base_url": "https://ai.t8star.cn/v1",
        "api_key": "sk-你的API密钥",
        "max_images": 4
      }
    }
  }
}
```

---

### 4️⃣ 硅基流动 API (SiliconFlow)

**官方网站**: https://siliconflow.cn/

**申请步骤**:
1. 访问 [硅基流动平台](https://cloud.siliconflow.cn/)
2. 注册并登录账号
3. 完成实名认证（必需）
4. 进入"API 管理"页面
5. 创建新的 API Key
6. 复制生成的密钥（格式：`sk-xxxxxx`）

**免费额度**:
- 新用户赠送免费额度
- 支持按量付费

**支持模型**:
- `Qwen/Qwen3-VL-32B-Instruct` - Qwen3-VL 32B 指令模型
- `Qwen/Qwen3-VL-235B-A22B-Instruct` - Qwen3-VL 235B-A22B 指令模型
- `Qwen/Qwen3-VL-235B-A22B-Thinking` - Qwen3-VL 235B-A22B 思维链模型

**特点**:
- OpenAI 兼容 API 格式
- 支持图像和视频理解
- 稳定的服务质量
- 国内访问速度快

**配置示例**:
```json
{
  "api": {
    "providers": {
      "硅基流动API": {
        "name": "siliconflow",
        "base_url": "https://api.siliconflow.cn/v1",
        "api_key": "sk-你的API密钥",
        "max_images": 4,
        "compression_quality": 85
      }
    }
  }
}
```

**使用说明**:
- 硅基流动使用 OpenAI 兼容的 API 格式
- 支持 base64 编码的图像和视频输入
- 建议图像大小不超过 15MB（编码后约 20MB）
- 视频文件建议压缩后上传

---

### 🔧 配置 API Key

**方法 1：编辑配置文件**
1. 打开 `ComfyUI_Qwen3-VL/Qwen3-VL-config.json`
2. 找到对应的 provider 配置
3. 将 `api_key` 字段替换为你的密钥
4. 保存文件并重启 ComfyUI

**方法 2：节点参数输入**
- 在节点的 `api_key` 参数中直接输入
- 优先级高于配置文件

**方法 3：环境变量**
```bash
export DASHSCOPE_API_KEY="sk-你的密钥"
```

---

## 📦 节点说明

### API 节点

#### 1. **Qwen3VL API** (基础版)
- **功能**: 调用云端 API 进行图像/视频分析
- **输入**:
  - `provider`: API 服务商（通义万像/Comfly/T8/硅基流动）
  - `model_name`: 模型选择
  - `prompt`: 文本提示词
  - `image`: 图像输入（可选）
  - `video`: 视频输入（可选）
  - `api_key`: API 密钥（可选）
  - `max_tokens`: 最大输出长度
  - `temperature`: 温度参数（0.0-2.0）
  - `top_p`: 核采样参数（0.0-1.0）
  - `stream`: 是否启用流式输出
- **输出**:
  - `text`: 模型响应文本
  - `raw_response`: 原始 JSON 响应

#### 2. **Qwen3VL API Advanced** (高级版)
- **功能**: 支持多图输入的高级 API 调用
- **额外输入**:
  - `image1` ~ `image4`: 最多 4 张图片
- **特性**:
  - 自动图像压缩（最大边长 2048px）
  - 智能图片数量限制
  - 更详细的错误提示

### 本地推理节点

#### 3. **Qwen3-VL Processor**
- **功能**: 本地模型推理
- **输入**:
  - `model_name`: 本地模型选择
  - `quantization`: 量化选项（none/4bit/8bit）
  - `attention_type`: 注意力机制类型
  - `prompt`: 文本提示
  - `image`: 图像输入
  - `video`: 视频输入
  - `temperature`: 温度参数
  - `top_p`: 核采样参数
  - `max_new_tokens`: 最大生成长度
  - `seed`: 随机种子
- **输出**:
  - `text`: 生成文本
  - `response`: 完整响应

### 工具节点

#### 4. **Load Video for Qwen3-VL**
- **功能**: 加载视频文件
- **参数**:
  - `video_path`: 视频路径
  - `fps`: 采样帧率
  - `max_frames`: 最大帧数

#### 5. **Combine Images for Qwen3-VL**
- **功能**: 合并多张图片
- **输入**: 最多 5 张图片
- **输出**: 合并后的图片列表

#### 6. **Display Qwen3-VL Response**
- **功能**: 显示模型响应
- **输入**: 文本响应
- **输出**: 格式化显示

---

## ⚙️ 配置说明

### 支持的模型

#### 云端 API 模型

| 模型名称 | 标识 | 服务商 | 特点 |
|---------|------|--------|------|
| Qwen3-VL 235B Instruct | `[Tongyi Wanxiang]qwen3-vl-235b-a22b-instruct` | 通义万像 | 指令微调，适合任务执行 |
| Qwen3-VL 235B | `[Comfly-T8]qwen3-vl-235b-a22b` | Comfly/T8 | 通用版本 |
| Qwen3-VL 235B Thinking | `[Tongyi Wanxiang]qwen3-vl-235b-a22b-thinking` | 通义万像 | 思维链推理 |
| Qwen-VL Max | `[Tongyi Wanxiang]qwen-vl-max` | 通义万像 | 最大能力版本 |
| Qwen-VL Plus | `[Tongyi Wanxiang]qwen-vl-plus` | 通义万像 | 平衡版本 |
| Qwen3-VL 32B Instruct | `[siliconflow]Qwen/Qwen3-VL-32B-Instruct` | 硅基流动 | 32B 指令模型，性价比高 |
| Qwen3-VL 235B-A22B Instruct | `[siliconflow]Qwen/Qwen3-VL-235B-A22B-Instruct` | 硅基流动 | 235B 大模型，高性能 |
| Qwen3-VL 235B-A22B Thinking | `[siliconflow]Qwen/Qwen3-VL-235B-A22B-Thinking` | 硅基流动 | 235B 思维链推理模型 |

#### 本地模型

| 模型名称 | 参数量 | VRAM 需求 | 特点 |
|---------|--------|----------|------|
| Qwen3-VL-4B-Instruct | 4B | ~8GB | 轻量级，适合入门 |
| Qwen3-VL-4B-Thinking | 4B | ~8GB | 思维链推理 |
| Qwen3-VL-8B-Instruct | 8B | ~16GB | 更强性能 |
| Qwen3-VL-8B-Thinking | 8B | ~16GB | 高级推理 |
| Qwen3-VL-4B-Instruct-FP8 | 4B | ~4GB | FP8 量化 |
| Qwen3-VL-8B-Instruct-FP8 | 8B | ~8GB | FP8 量化 |

### 参数说明

#### 生成参数

| 参数 | 范围 | 默认值 | 说明 |
|------|------|--------|------|
| `temperature` | 0.0-2.0 | 0.7 | 控制随机性，越高越创造性 |
| `top_p` | 0.0-1.0 | 0.8 | 核采样，控制多样性 |
| `top_k` | 0-100 | 20 | Top-K 采样 |
| `max_tokens` | 1-8192 | 1024 | 最大输出长度 |
| `repetition_penalty` | 0.0-2.0 | 1.0 | 重复惩罚 |

#### 视觉参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `min_pixels` | 256×32×32 | 最小视觉 tokens |
| `max_pixels` | 1280×32×32 | 最大视觉 tokens |
| `max_size` | 2048 | 图像最大边长（自动压缩） |

---

## 💡 使用示例

### 示例 1：单图分析（API 模式）

**工作流**:
```
LoadImage → Qwen3VL API
```

**配置**:
- Provider: `通义万像API`
- Model: `[Tongyi Wanxiang]qwen3-vl-235b-a22b-instruct`
- Prompt: `请详细描述这张图片的内容，包括主要物体、颜色、场景等`
- Temperature: `0.7`
- Max Tokens: `2048`

**应用场景**:
- 图片内容描述
- 物体识别
- 场景理解
- OCR 文字识别

---

### 示例 2：多图对比（API Advanced）

**工作流**:
```
LoadImage (图1) → Qwen3VL API Advanced
LoadImage (图2) → Qwen3VL API Advanced
LoadImage (图3) → Qwen3VL API Advanced
```

**配置**:
- Provider: `Comfly API`
- Model: `[Comfly-T8]qwen3-vl-235b-a22b`
- Prompt: `对比这几张图片的异同点，分析它们的共同特征和差异`
- Max Images: `4`

**应用场景**:
- 产品对比
- 图片相似度分析
- 变化检测
- 质量对比

---

### 示例 3：视频理解

**工作流**:
```
Load Video for Qwen3-VL → Qwen3VL API
```

**配置**:
- Video Path: `path/to/video.mp4`
- FPS: `2` (每秒采样 2 帧)
- Max Frames: `128`
- Prompt: `总结这个视频的主要内容和关键事件`

**应用场景**:
- 视频摘要
- 动作识别
- 事件检测
- 内容审核

---

### 示例 4：思维链推理

**工作流**:
```
LoadImage → Qwen3VL API
```

**配置**:
- Model: `[Tongyi Wanxiang]qwen3-vl-235b-a22b-thinking`
- Prompt: `这是一道数学题的图片，请一步步分析并给出解答过程`
- Temperature: `0.3` (降低随机性)

**应用场景**:
- 数学题解答
- 逻辑推理
- 复杂问题分析
- 教育辅导

---

### 示例 5：本地模型推理

**工作流**:
```
LoadImage → Qwen3-VL Processor
```

**配置**:
- Model: `Qwen3-VL-4B-Instruct-FP8`
- Quantization: `8bit`
- Attention Type: `flash_attention_2`
- Prompt: `描述图片内容`

**应用场景**:
- 离线使用
- 数据隐私保护
- 批量处理
- 自定义微调

---

## 📋 工作流示例文件

项目提供了完整的工作流 JSON 文件，位于 `examples/` 目录：

### API 工作流
- `api_workflow_single_image.json` - 单图分析
- `api_workflow_multi_image.json` - 多图对比
- `api_workflow_video.json` - 视频理解
- `api_workflow_text_only.json` - 纯文本对话
- `api_workflow_streaming.json` - 流式输出
- `api_workflow_thinking_mode.json` - 思维链模式
- `api_workflow_advanced_mixed.json` - 高级混合模式

### 本地推理工作流
- `examples_workflow_single_image.json` - 单图分析
- `examples_workflow_multi_image.json` - 多图处理
- `examples_workflow_video.json` - 视频处理
- `examples_workflow_text_only.json` - 文本生成

### 使用方法
1. 打开 ComfyUI
2. 点击 "Load" 按钮
3. 选择 `examples/` 目录下的 JSON 文件
4. 根据需要修改提示词和参数
5. 点击 "Queue Prompt" 运行

---

## 🎯 性能优化建议

### 💾 内存优化

**API 模式**:
- ✅ 无需本地显存
- ✅ 自动图像压缩（2048px）
- ✅ 智能图片数量限制

**本地推理模式**:
| 优化方法 | VRAM 节省 | 性能影响 |
|---------|----------|---------|
| 使用 FP8 模型 | ~50% | 轻微 |
| 启用 8bit 量化 | ~60% | 中等 |
| 启用 4bit 量化 | ~75% | 较大 |
| 使用 4B 模型 | ~50% | 中等 |
| 降低 max_pixels | 10-30% | 轻微 |

**推荐配置**:
```python
# 8GB VRAM
Model: Qwen3-VL-4B-Instruct-FP8
Quantization: 8bit
Max Pixels: 512×32×32

# 16GB VRAM
Model: Qwen3-VL-8B-Instruct-FP8
Quantization: none
Max Pixels: 1280×32×32

# 24GB+ VRAM
Model: Qwen3-VL-8B-Instruct
Quantization: none
Attention: flash_attention_2
```

---

### ⚡ 速度优化

**API 模式**:
- 使用流式输出（`stream=True`）获得更快响应
- 选择地理位置近的服务商
- 启用代理加速（如需要）

**本地推理模式**:
| 优化方法 | 速度提升 | 要求 |
|---------|---------|------|
| flash_attention_2 | 2-3x | CUDA 11.8+, Ampere+ GPU |
| 降低 max_new_tokens | 线性 | 无 |
| 降低 max_pixels | 20-40% | 无 |
| 使用 FP8 模型 | 10-20% | 无 |

---

### 🎨 质量优化

**参数调优**:
```python
# 事实性任务（描述、识别）
Temperature: 0.1-0.3
Top_P: 0.8
Model: Instruct 版本

# 创造性任务（写作、创意）
Temperature: 0.7-1.0
Top_P: 0.9
Model: Instruct 版本

# 复杂推理（数学、逻辑）
Temperature: 0.3-0.5
Top_P: 0.8
Model: Thinking 版本
```

**提示词优化**:
- ✅ 使用清晰、具体的指令
- ✅ 提供上下文信息
- ✅ 分步骤描述复杂任务
- ❌ 避免模糊、歧义的表达

---

## ❓ 常见问题

### Q1: API 调用失败，返回 401/403 错误？

**A**: 检查 API Key 配置
```json
// 确保 API Key 正确填写
"api_key": "sk-你的完整密钥"

// 检查服务商是否正确
"provider": "通义万像API"  // 必须与配置文件中的名称一致
```

---

### Q2: 图片太大导致 API 调用失败？

**A**: 插件已自动处理
- ✅ 自动压缩到 2048px（最大边长）
- ✅ 保持宽高比
- ✅ 使用高质量 LANCZOS 算法

如仍有问题，可手动调整：
```json
"media": {
  "image": {
    "max_size_mb": 9,
    "compression_quality": 85
  }
}
```

---

### Q3: 本地模型下载失败？

**A**: 解决方法
```bash
# 方法 1: 使用镜像站
export HF_ENDPOINT=https://hf-mirror.com

# 方法 2: 手动下载
huggingface-cli download Qwen/Qwen3-VL-4B-Instruct \
  --local-dir ComfyUI/models/qwen3vl/Qwen3-VL-4B-Instruct

# 方法 3: 使用代理
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
```

---

### Q4: 显存不足（OOM）错误？

**A**: 降低显存使用
1. 使用 FP8 量化模型
2. 启用 8bit/4bit 量化
3. 降低 `max_pixels` 参数
4. 使用 4B 模型替代 8B
5. 关闭其他占用显存的程序

---

### Q5: 视频处理速度慢？

**A**: 优化建议
```python
# 降低采样率
FPS: 1-2  # 每秒 1-2 帧

# 限制帧数
Max Frames: 64-128

# 使用 API 模式
Provider: 通义万像API  # 云端处理更快
```

---

### Q6: 多图分析时图片顺序混乱？

**A**: 使用 API Advanced 节点
- 明确的 `image1`, `image2`, `image3`, `image4` 输入
- 保证顺序一致性
- 最多支持 4 张图片

---

### Q7: 代理设置不生效？

**A**: 检查配置
```json
{
  "api": {
    "proxy": "http://127.0.0.1:7897",  // 设置代理
    "disable_proxy_for_t8": false      // 是否对 T8 禁用代理
  }
}
```

或在节点中设置环境变量：
```python
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'
```

---

### Q8: 流式输出不工作？

**A**: 确认配置
```json
{
  "features": {
    "enable_streaming": true  // 启用流式输出
  }
}
```

节点参数：
```python
stream: True  // 勾选启用
```

---

## 📊 模型对比

### API 模型对比

| 模型 | 参数量 | 速度 | 质量 | 成本 | 推荐场景 |
|------|--------|------|------|------|---------|
| qwen-vl-plus | 未知 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 💰 | 日常使用 |
| qwen-vl-max | 未知 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰 | 高质量需求 |
| qwen3-vl-235b-instruct | 235B | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰 | 专业任务 |
| qwen3-vl-235b-thinking | 235B | ⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰💰 | 复杂推理 |
| Qwen3-VL-32B-Instruct | 32B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰 | 性价比之选 |
| Qwen3-VL-235B-A22B-Instruct | 235B | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰 | 高性能需求 |
| Qwen3-VL-235B-A22B-Thinking | 235B | ⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰💰 | 思维链推理 |

### 本地模型对比

| 模型 | VRAM | 速度 | 质量 | 推荐场景 |
|------|------|------|------|---------|
| 4B-Instruct-FP8 | ~4GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 入门/测试 |
| 4B-Instruct | ~8GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 日常使用 |
| 8B-Instruct-FP8 | ~8GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 平衡选择 |
| 8B-Instruct | ~16GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 高质量 |
| 4B-Thinking | ~8GB | ⭐⭐⭐ | ⭐⭐⭐⭐ | 推理任务 |
| 8B-Thinking | ~16GB | ⭐⭐ | ⭐⭐⭐⭐⭐ | 复杂推理 |

---

## 🔄 更新日志

### v2.0.0 (2025-01-21)
- ✨ 新增 API 调用支持（通义万像、Comfly、T8）
- ✨ 新增流式输出功能
- ✨ 新增思维链模式
- ✨ 自动图像压缩（2048px）
- ✨ 多图分析支持（最多 4 张）
- 🐛 修复代理设置问题
- 🐛 修复模型名称显示问题
- 📝 完善文档和示例

### v1.0.0 (2024-12-01)
- 🎉 初始版本发布
- ✅ 本地模型推理支持
- ✅ 图像/视频输入支持
- ✅ 基础工作流示例

---

## 📄 许可证

本项目采用 **Apache 2.0** 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- **Qwen3-VL** - Alibaba Cloud Qwen Team
- **ComfyUI** - comfyanonymous
- **参考实现** - IuvenisSapiens

---

## 📞 支持与反馈

- **GitHub Issues**: [提交问题](https://github.com/yourusername/ComfyUI_Qwen3-VL/issues)
- **讨论区**: [参与讨论](https://github.com/yourusername/ComfyUI_Qwen3-VL/discussions)
- **文档**: [查看完整文档](./docs/)

---

## 💬 联系支持

### 微信交流

如有问题或建议，欢迎添加微信交流：

<div align="center">

<table>
<tr>
<td align="center">
<img src="assets/wechat_qrcode.png" width="200" alt="微信二维码"><br>
<b>微信二维码</b><br>
扫码添加微信
</td>
</tr>
</table>

</div>

### ☕ 赞助支持

如果这个项目对你有帮助，欢迎请作者喝杯咖啡 ☕

<div align="center">

<table>
<tr>
<td align="center">
<img src="assets/wechat_pay.png" width="200" alt="微信收款码"><br>
<b>微信赞赏</b><br>
感谢您的支持！
</td>
</tr>
</table>

</div>

> **说明**：赞助完全自愿，不影响项目的开源和免费使用。您的支持将用于项目的持续维护和改进。

---

## 🌟 Star History

如果这个项目对你有帮助，请给个 ⭐ Star！

---

<div align="center">

**Made with ❤️ for ComfyUI Community**

[⬆ 回到顶部](#comfyui-qwen3-vl-integration)

</div>

