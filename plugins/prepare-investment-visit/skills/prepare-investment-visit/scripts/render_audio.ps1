[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InputTextPath,
    [Parameter(Mandatory = $true)]
    [string]$OutputPath,
    [string]$VoiceName = "",
    [ValidateRange(-10, 10)]
    [int]$Rate = 0
)

$ErrorActionPreference = 'Stop'
$inputFile = (Resolve-Path -LiteralPath $InputTextPath).Path
$text = [System.IO.File]::ReadAllText($inputFile, [System.Text.Encoding]::UTF8).Trim()
if ([string]::IsNullOrWhiteSpace($text)) { throw 'Podcast script is empty.' }
$target = [System.IO.Path]::GetFullPath($OutputPath)
$parent = [System.IO.Path]::GetDirectoryName($target)
if (-not [string]::IsNullOrWhiteSpace($parent)) { [System.IO.Directory]::CreateDirectory($parent) | Out-Null }

Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $voices = @($speaker.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo })
    if ($VoiceName) {
        if (-not ($voices.Name -contains $VoiceName)) { throw "Requested voice is not installed: $VoiceName" }
        $speaker.SelectVoice($VoiceName)
    }
    else {
        $chineseVoice = $voices | Where-Object { $_.Culture.Name -eq 'zh-CN' } | Select-Object -First 1
        if (-not $chineseVoice) { throw 'No installed zh-CN speech voice was found.' }
        $speaker.SelectVoice($chineseVoice.Name)
    }
    $speaker.Rate = $Rate
    $speaker.Volume = 100
    $speaker.SetOutputToWaveFile($target)
    $speaker.Speak($text)
}
finally {
    try { $speaker.SetOutputToNull() } catch { }
    $speaker.Dispose()
}
$audio = Get-Item -LiteralPath $target
if ($audio.Length -le 44) { throw 'Audio rendering produced an empty WAV file.' }
Write-Output ("AUDIO_OK" + [char]9 + $audio.FullName + [char]9 + $audio.Length)
