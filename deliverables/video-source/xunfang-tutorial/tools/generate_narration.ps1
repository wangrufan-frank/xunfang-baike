$ErrorActionPreference = 'Stop'

$projectRoot = (Get-Location).Path
$audioDir = Join-Path $projectRoot 'audio'
New-Item -ItemType Directory -Force -Path $audioDir | Out-Null

$beats = @(
    '需要查找一项巡防知识时，还要在多个文件和课件里反复翻找吗？巡防百科把常用的警务知识整理到一个统一入口，让资料更容易找到，也更方便持续更新。',
    '打开巡防百科网站，首页集中展示六大业务模块：装备介绍、巡防勤务、警务训练、警情处置、法条规范和走访送教。知道自己要查哪一类内容时，直接点击对应模块即可进入。',
    '以警情处置为例。进入模块后，页面会按照常见场景列出已经整理的专题。选择具体条目，就能查看处置流程、注意事项和相关依据。这样的分类方式，适合按工作场景逐层查找。',
    '如果不确定内容属于哪个模块，可以使用站内搜索。输入警情、装备、法规或其他关键词，网站会在已有内容中匹配相关页面。点击搜索结果，就可以直接进入对应主题。',
    '详情页把核心内容整理成标题、标签和步骤卡片。重点流程可以按顺序阅读，图片用于说明动作和位置，视频用于辅助理解训练类内容。使用时，先看核心结论，再根据需要展开详细说明。',
    '巡防百科的使用路径很简单：进入网站，选择模块或输入关键词，再查看对应要点。后续内容会根据实际需要持续补充和完善。访问网址，三 W 点，巡防百科点 C N。'
)

Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.SelectVoice('Microsoft Huihui Desktop')
$speaker.Rate = -1
$speaker.Volume = 100

for ($i = 0; $i -lt $beats.Count; $i++) {
    $path = Join-Path $audioDir ('beat-{0}.wav' -f ($i + 1))
    $speaker.SetOutputToWaveFile($path)
    $speaker.Speak($beats[$i])
    $speaker.SetOutputToNull()
}

$speaker.Dispose()
Write-Output "Generated $($beats.Count) narration clips in $audioDir"
