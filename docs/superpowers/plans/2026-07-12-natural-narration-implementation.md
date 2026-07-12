# 自然旁白替换 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为巡防百科教学视频生成更自然的普通话女声旁白，并输出仅保留新版的可播放 MP4。

**Architecture:** 保留现有 H.264 画面轨道，单独生成带语义停顿的神经语音 WAV，再以 FFmpeg 将其编码为 AAC 并封装回 MP4。新音频时长作为输出时长基准，不改动网页截图、镜头内容或 PPT。

**Tech Stack:** Edge 神经语音、PowerShell、FFmpeg、FFprobe、H.264/AAC MP4。

## Global Constraints

- 使用普通话神经女声，语速为约 0.92 倍自然语速。
- 保留六段讲解的事实内容、深蓝米白金色视觉和现有视频画面。
- 输出 1920×1080、30fps、H.264 视频和 AAC 音轨。
- 仅在新版通过音视频校验后删除旧版成片。

---

### Task 1: 生成自然旁白音频

**Files:**
- Create: `deliverables/video-source/xunfang-tutorial/narration-natural.txt`
- Create: `deliverables/video-source/xunfang-tutorial/narration-natural.wav`

**Interfaces:**
- Consumes: `deliverables/video-source/xunfang-tutorial/SCRIPT.md`
- Produces: 单声道 WAV 旁白，用于 MP4 音频替换。

- [ ] **Step 1: 编写带语义停顿的旁白稿**

将六段脚本改为口语化文本；每段使用短句与中文标点控制停顿，并将网址写为“巡防百科点 C N”。

- [ ] **Step 2: 生成神经女声 WAV**

运行：

```powershell
edge-tts --voice zh-CN-XiaoxiaoNeural --rate=-8% --file narration-natural.txt --write-media narration-natural.mp3
ffmpeg -y -i narration-natural.mp3 -ac 1 -ar 22050 narration-natural.wav
```

预期：生成可播放的普通话女声 WAV，句间有自然停顿。

- [ ] **Step 3: 检查音频参数**

运行：

```powershell
ffprobe -v error -show_entries format=duration:stream=codec_name,codec_type -of default=noprint_wrappers=1 narration-natural.wav
```

预期：显示 `codec_name=pcm_s16le`、`codec_type=audio` 和有效时长。

### Task 2: 封装新版成片并替换旧版

**Files:**
- Create: `deliverables/xunfang-tutorial-natural.mp4`
- Delete after validation: `deliverables/xunfang-tutorial-final.mp4`

**Interfaces:**
- Consumes: `deliverables/xunfang-tutorial-final.mp4` 的 H.264 画面轨道与 `narration-natural.wav`。
- Produces: 带自然旁白的最终 MP4。

- [ ] **Step 1: 写入新版 MP4**

运行：

```powershell
ffmpeg -y -i xunfang-tutorial-final.mp4 -i narration-natural.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest xunfang-tutorial-natural.mp4
```

预期：视频画面直接复制，音频转为 AAC，成片时长与旁白一致。

- [ ] **Step 2: 验证视频、音频与时长**

运行：

```powershell
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate:format=duration,size -of default=noprint_wrappers=1 xunfang-tutorial-natural.mp4
```

预期：视频为 `h264`、1920×1080、30fps；音频为 `aac`；时长大于 120 秒。

- [ ] **Step 3: 删除旧版成片并提交**

仅在步骤 2 通过后删除 `deliverables/xunfang-tutorial-final.mp4`，并提交新旁白稿、自然旁白音频、最终 MP4 和制作脚本。
