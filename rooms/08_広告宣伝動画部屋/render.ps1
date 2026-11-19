$ErrorActionPreference = 'Stop'
Push-Location (Join-Path $PSScriptRoot 'project')
try {
    $chromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    if (-not (Test-Path -LiteralPath $chromePath)) { throw 'Chrome is required; change chromePath to the installed browser.' }
    node node_modules/@remotion/cli/remotion-cli.js render src/index.ts Portrait15 ../masters/kaononaiharu_vertical_15s.mp4 --codec=h264 --crf=18 --pixel-format=yuv420p --audio-codec=aac --audio-bitrate=192k --concurrency=2 --browser-executable=$chromePath
    if ($LASTEXITCODE -ne 0) { throw 'Portrait render failed' }
    node node_modules/@remotion/cli/remotion-cli.js render src/index.ts Landscape30 ../masters/kaononaiharu_horizontal_30s.mp4 --codec=h264 --crf=18 --pixel-format=yuv420p --audio-codec=aac --audio-bitrate=192k --concurrency=2 --browser-executable=$chromePath
    if ($LASTEXITCODE -ne 0) { throw 'Landscape render failed' }
    python ../finalize.py
    if ($LASTEXITCODE -ne 0) { throw 'Finalization failed' }
    python ../verify.py
    if ($LASTEXITCODE -ne 0) { throw 'Verification failed' }
} finally { Pop-Location }
