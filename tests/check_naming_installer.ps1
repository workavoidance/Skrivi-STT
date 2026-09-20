# Only run against a disposable GitHub-hosted account, never a user's installation.
$ErrorActionPreference = 'Stop'
if ($env:GITHUB_ACTIONS -ne 'true' -or $env:RUNNER_ENVIRONMENT -ne 'github-hosted') {
    throw 'Naming installer tests require a disposable GitHub-hosted runner.'
}
$root = Split-Path $PSScriptRoot -Parent
$installers = @(Get-ChildItem (Join-Path $root 'dist/installer') -Filter '*-setup.exe')
if ($installers.Count -ne 1) { throw 'Expected exactly one built installer.' }
$appRoot = Join-Path $env:LOCALAPPDATA 'Programs\Skrivi'
$settingsRoot = Join-Path $env:APPDATA 'Skrivi'
$modelsRoot = Join-Path $env:LOCALAPPDATA 'Skrivi\models'
foreach ($target in @($appRoot, $settingsRoot, $modelsRoot)) {
    if (Test-Path -LiteralPath $target) { throw "Test requires an empty runner: $target" }
}
function Install-TestApp {
    $process = Start-Process -FilePath $installers[0].FullName -ArgumentList '/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART' -WindowStyle Hidden -PassThru
    if (!$process.WaitForExit(180000) -or $process.ExitCode -ne 0) { throw 'Setup failed.' }
}
Install-TestApp
$app = Join-Path $appRoot 'Skrivi.exe'
if ($env:SKRIVI_EXPECTED_SIGNER) {
    & (Join-Path $root 'tools\sign_windows.ps1') -VerifyOnly -Thumbprint $env:SKRIVI_EXPECTED_SIGNER -Path @($app, (Join-Path $appRoot 'unins000.exe'))
}
if (!(Test-Path -LiteralPath $app)) { throw 'Stable executable path changed.' }
$menu = Join-Path ([Environment]::GetFolderPath('Programs')) 'Skrivi'
$desktop = [Environment]::GetFolderPath('Desktop')
$shellLink = New-Object -ComObject WScript.Shell
foreach ($folder in @($menu, $desktop)) {
    $link = $shellLink.CreateShortcut((Join-Path $folder 'Skrivi.lnk'))
    $link.TargetPath = $app
    $link.Save()
}
New-Item -ItemType Directory -Force -Path $settingsRoot,$modelsRoot | Out-Null
$settings = Join-Path $settingsRoot 'settings.json'
$model = Join-Path $modelsRoot 'naming-preservation.bin'
Set-Content -LiteralPath $settings -Value '{"naming_fixture":true}'
Set-Content -LiteralPath $model -Value 'Never overwrite an existing model during rename.'
$before = @{}
foreach ($file in @($settings,$model)) { $before[$file] = (Get-FileHash -LiteralPath $file).Hash }
Install-TestApp
foreach ($folder in @($menu,$desktop)) {
    if (Test-Path -LiteralPath (Join-Path $folder 'Skrivi.lnk')) { throw 'Old owned shortcut remains.' }
    $newPath = Join-Path $folder 'Skrivi Snakk.lnk'
    if (!(Test-Path -LiteralPath $newPath)) { throw 'New shortcut missing.' }
    if ($shellLink.CreateShortcut($newPath).TargetPath -ine $app) { throw 'Shortcut target changed.' }
}
foreach ($file in $before.Keys) {
    if ((Get-FileHash -LiteralPath $file).Hash -ne $before[$file]) { throw 'Reinstall changed user data.' }
}
$process = Start-Process -FilePath (Join-Path $appRoot 'unins000.exe') -ArgumentList '/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART' -WindowStyle Hidden -PassThru
if (!$process.WaitForExit(120000) -or $process.ExitCode -ne 0) { throw 'Uninstall failed.' }
foreach ($folder in @($menu,$desktop)) {
    if (Test-Path -LiteralPath (Join-Path $folder 'Skrivi Snakk.lnk')) { throw 'Uninstall left a renamed shortcut.' }
}
foreach ($file in $before.Keys) {
    if ((Get-FileHash -LiteralPath $file).Hash -ne $before[$file]) { throw 'Uninstall changed user data.' }
}
Write-Output 'Naming: install, legacy shortcut migration, reinstall and data-preserving uninstall passed.'
