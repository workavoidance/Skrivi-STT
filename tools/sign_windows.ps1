param(
    [Parameter(Mandatory = $true)][string[]]$Path,
    [Parameter(Mandatory = $true)][string]$Thumbprint,
    [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'
$Thumbprint = ($Thumbprint -replace '\s', '').ToUpperInvariant()
if ($Thumbprint -notmatch '^[0-9A-F]{40}$') { throw 'Expected a SHA-1 certificate thumbprint.' }
$SignTool = Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin\*\x64\signtool.exe" |
    Sort-Object FullName -Descending | Select-Object -First 1
if (-not $SignTool) { throw 'Windows SDK SignTool was not found.' }

foreach ($FilePath in $Path) {
    $File = Get-Item -LiteralPath $FilePath -ErrorAction Stop
    if ($File.PSIsContainer -or $File.Extension -ne '.exe') { throw "Expected an executable: $FilePath" }
    if (-not $VerifyOnly) {
        & $SignTool.FullName sign /sha1 $Thumbprint /fd SHA256 /tr http://time.certum.pl /td SHA256 $File.FullName
        if ($LASTEXITCODE -ne 0) { throw "Signing failed: $FilePath" }
    }
    & $SignTool.FullName verify /pa /all /v $File.FullName
    if ($LASTEXITCODE -ne 0) { throw "Signature verification failed: $FilePath" }
    $Signature = Get-AuthenticodeSignature -LiteralPath $File.FullName
    if ($Signature.Status -ne 'Valid') { throw "Invalid signature: $FilePath" }
    if ($Signature.SignerCertificate.Thumbprint -ne $Thumbprint) { throw "Unexpected signer: $FilePath" }
    if (-not $Signature.TimeStamperCertificate) { throw "Missing timestamp: $FilePath" }
    Write-Host "Verified signed and timestamped executable: $FilePath"
}
