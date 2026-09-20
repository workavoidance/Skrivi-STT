#define MyAppName "Skrivi Snakk"
#define MyAppVersion GetEnv("SKRIVI_INSTALLER_VERSION")
#define MySourceDir GetEnv("SKRIVI_INSTALLER_SOURCE")
#define MyOutputDir GetEnv("SKRIVI_INSTALLER_OUTPUT")
#define MyProjectRoot GetEnv("SKRIVI_PROJECT_ROOT")

[Setup]
#ifdef SignedBuild
SignTool=skrivi
SignedUninstaller=yes
#endif
AppId={{B17E37FA-9342-4B72-96C4-76F57498A44E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=Skrivi
AppPublisherURL=https://skrivi.no/
AppSupportURL=https://github.com/workavoidance/Skrivi-STT/issues
AppUpdatesURL=https://github.com/workavoidance/Skrivi-STT/releases
DefaultDirName={localappdata}\Programs\Skrivi
DefaultGroupName=Skrivi
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
MinVersion=10.0.22000
OutputDir={#MyOutputDir}
OutputBaseFilename=Skrivi-Snakk-{#MyAppVersion}-windows-x64-setup
SetupIconFile={#MyProjectRoot}\assets\skrivi.ico
UninstallDisplayIcon={app}\Skrivi.exe
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes
RestartApplications=no
SetupLogging=yes
LicenseFile={#MyProjectRoot}\LICENSE
ChangesAssociations=no
ChangesEnvironment=no
UsedUserAreasWarning=no

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[InstallDelete]
Type: filesandordirs; Name: "{app}\runtime"

[Files]
Source: "{#MySourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#MyProjectRoot}\README.md"; DestDir: "{app}\documentation"; Flags: ignoreversion
Source: "{#MyProjectRoot}\LICENSE"; DestDir: "{app}\documentation"; Flags: ignoreversion
Source: "{#MyProjectRoot}\CHANGELOG.md"; DestDir: "{app}\documentation"; Flags: ignoreversion
Source: "{#MyProjectRoot}\THIRD_PARTY_NOTICES.md"; DestDir: "{app}\documentation"; Flags: ignoreversion

[Icons]
Name: "{group}\Skrivi Snakk"; Filename: "{app}\Skrivi.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall Skrivi Snakk"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Skrivi Snakk"; Filename: "{app}\Skrivi.exe"; WorkingDir: "{app}"; Check: WantDesktopShortcut

[Run]
Filename: "{app}\Skrivi.exe"; Description: "Launch Skrivi Snakk"; Flags: nowait postinstall skipifsilent

[Code]
function WantDesktopShortcut: Boolean;
var
  Shell, Link: Variant;
  OldPath: String;
begin
  Result := WizardIsTaskSelected('desktopicon');
  OldPath := ExpandConstant('{autodesktop}\Skrivi.lnk');
  if Result or not FileExists(OldPath) then Exit;
  try
    Shell := CreateOleObject('WScript.Shell');
    Link := Shell.CreateShortcut(OldPath);
    Result := CompareText(Link.TargetPath, ExpandConstant('{app}\Skrivi.exe')) = 0;
  except
    Result := False;
  end;
end;

procedure RenameOwnedShortcut(OldPath, NewPath, ExpectedTarget: String);
var
  Shell, Link: Variant;
begin
  if not FileExists(OldPath) then Exit;
  try
    Shell := CreateOleObject('WScript.Shell');
    Link := Shell.CreateShortcut(OldPath);
    if CompareText(Link.TargetPath, ExpectedTarget) <> 0 then Exit;
    if not FileExists(NewPath) then
      if not FileCopy(OldPath, NewPath, True) then Exit;
    DeleteFile(OldPath);
  except
    Log('Could not migrate an old Skrivi shortcut; it was left in place.');
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep <> ssPostInstall then Exit;
  RenameOwnedShortcut(ExpandConstant('{group}\Skrivi.lnk'),
    ExpandConstant('{group}\Skrivi Snakk.lnk'), ExpandConstant('{app}\Skrivi.exe'));
  RenameOwnedShortcut(ExpandConstant('{group}\Uninstall Skrivi.lnk'),
    ExpandConstant('{group}\Uninstall Skrivi Snakk.lnk'), ExpandConstant('{uninstallexe}'));
  RenameOwnedShortcut(ExpandConstant('{autodesktop}\Skrivi.lnk'),
    ExpandConstant('{autodesktop}\Skrivi Snakk.lnk'), ExpandConstant('{app}\Skrivi.exe'));
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  RegisteredCommand: String;
  InstalledCommand: String;
begin
  if CurUninstallStep <> usUninstall then
    Exit;

  InstalledCommand := '"' + ExpandConstant('{app}\Skrivi.exe') + '"';
  if RegQueryStringValue(
    HKCU,
    'Software\Microsoft\Windows\CurrentVersion\Run',
    'Skrivi',
    RegisteredCommand
  ) and ((CompareText(RegisteredCommand, InstalledCommand) = 0) or
    (CompareText(RegisteredCommand, InstalledCommand + ' --tray') = 0)) then
    RegDeleteValue(
      HKCU,
      'Software\Microsoft\Windows\CurrentVersion\Run',
      'Skrivi'
    );
end;
