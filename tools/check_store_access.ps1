$ErrorActionPreference = 'Stop'

foreach ($name in @('AZURE_AD_APPLICATION_CLIENT_ID', 'AZURE_AD_APPLICATION_SECRET', 'AZURE_AD_TENANT_ID', 'SELLER_ID')) {
    if (-not [Environment]::GetEnvironmentVariable($name)) { throw "Missing GitHub secret: $name" }
}
$tenant = [guid]::Parse($env:AZURE_AD_TENANT_ID).ToString()
$client = [guid]::Parse($env:AZURE_AD_APPLICATION_CLIENT_ID).ToString()
try {
    $token = Invoke-RestMethod -Method Post -Uri "https://login.microsoftonline.com/$tenant/oauth2/token" -Body @{
        grant_type = 'client_credentials'
        client_id = $client
        client_secret = $env:AZURE_AD_APPLICATION_SECRET
        resource = 'https://manage.devcenter.microsoft.com'
    }
} catch {
    throw 'Microsoft authentication failed. Check the tenant, client ID, and unexpired client secret.'
}
if (-not $token.access_token) { throw 'Microsoft returned no access token.' }
Write-Output "::add-mask::$($token.access_token)"
try {
    $app = Invoke-RestMethod -Uri 'https://manage.devcenter.microsoft.com/v1.0/my/applications/9P42NBXD8W36' -Headers @{
        Authorization = "Bearer $($token.access_token)"
    }
} catch {
    throw 'Authentication succeeded, but Store app access failed. Check Partner Center permissions and API eligibility.'
}
if ($app.id -ne '9P42NBXD8W36' -or $app.packageIdentityName -ne 'Skrivi.Skrivi' -or $app.publisherName -ne 'CN=EF3D997F-87B2-4AD0-B65B-877EE1632E65') {
    throw 'Store app identity does not match the Skrivi Snakk package.'
}
$published = [bool]$app.lastPublishedApplicationSubmission.id
$pending = [bool]$app.pendingApplicationSubmission.id
$summary = @(
    'Microsoft authentication and Skrivi Snakk app access succeeded.',
    "Previously published submission: $published",
    "Pending submission or draft: $pending"
)
$summary | Write-Output
if ($env:GITHUB_STEP_SUMMARY) { $summary | Add-Content $env:GITHUB_STEP_SUMMARY }
if ($env:STORE_SUBMIT -eq 'true') {
    if (-not $published) { throw 'Complete the first Store submission in Partner Center before automating updates.' }
    if ($pending) { throw 'A Store draft or submission already exists. Resolve it in Partner Center; automation will not replace it.' }
}
