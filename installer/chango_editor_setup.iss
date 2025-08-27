[Setup]
; 应用程序信息
AppId={{C4F8D9E2-3A5B-4C7E-8F1A-2D3E4F5G6H7I}
AppName=Chango Editor
AppVersion=1.0.0
AppVerName=Chango Editor 1.0.0
AppPublisher=Chango Team
AppPublisherURL=https://github.com/aweng1977/chango/chango-editor
AppSupportURL=https://github.com/aweng1977/chango/chango-editor/issues
AppUpdatesURL=https://github.com/aweng1977/chango/chango-editor/releases
AppCopyright=© 2024 Chango Team

; 默认安装目录
DefaultDirName={autopf}\Chango Editor
DefaultGroupName=Chango Editor
AllowNoIcons=yes

; 许可证和信息文件
LicenseFile=..\LICENSE
InfoBeforeFile=installer\install_info.txt
InfoAfterFile=installer\install_complete.txt

; 输出设置
OutputDir=..\dist\installer
OutputBaseFilename=ChangoEditor-Setup-v1.0.0
SetupIconFile=..\resources\icons\chango_editor.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; 系统要求
MinVersion=0,6.1sp1
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; 特权要求
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; 界面设置
WizardImageFile=installer\wizard_image.bmp
WizardSmallImageFile=installer\wizard_small.bmp

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1
Name: "associate"; Description: "关联常用代码文件格式"; GroupDescription: "文件关联:"; Flags: unchecked

[Files]
; 主程序文件
Source: "..\dist\ChangoEditor.exe"; DestDir: "{app}"; Flags: ignoreversion
; 许可证文件
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
; 说明文件
Source: "..\README.md"; DestDir: "{app}"; DestName: "README.txt"; Flags: ignoreversion
; 示例文件
Source: "..\test_files\*"; DestDir: "{app}\examples"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; 开始菜单图标
Name: "{group}\Chango Editor"; Filename: "{app}\ChangoEditor.exe"; IconFilename: "{app}\ChangoEditor.exe"
Name: "{group}\示例文件"; Filename: "{app}\examples"
Name: "{group}\使用说明"; Filename: "{app}\README.txt"
Name: "{group}\{cm:UninstallProgram,Chango Editor}"; Filename: "{uninstallexe}"

; 桌面图标
Name: "{autodesktop}\Chango Editor"; Filename: "{app}\ChangoEditor.exe"; Tasks: desktopicon

; 快速启动图标
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Chango Editor"; Filename: "{app}\ChangoEditor.exe"; Tasks: quicklaunchicon

[Registry]
; 文件关联 - Python文件
Root: HKCU; Subkey: "SOFTWARE\Classes\.py\OpenWithProgids"; ValueType: string; ValueName: "ChangoEditor.py"; ValueData: ""; Flags: uninsdeletevalue; Tasks: associate
Root: HKCU; Subkey: "SOFTWARE\Classes\ChangoEditor.py"; ValueType: string; ValueName: ""; ValueData: "Python文件"; Flags: uninsdeletekey; Tasks: associate
Root: HKCU; Subkey: "SOFTWARE\Classes\ChangoEditor.py\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\ChangoEditor.exe,0"; Tasks: associate
Root: HKCU; Subkey: "SOFTWARE\Classes\ChangoEditor.py\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\ChangoEditor.exe"" ""%1"""; Tasks: associate

; 文件关联 - JavaScript文件
Root: HKCU; Subkey: "SOFTWARE\Classes\.js\OpenWithProgids"; ValueType: string; ValueName: "ChangoEditor.js"; ValueData: ""; Flags: uninsdeletevalue; Tasks: associate
Root: HKCU; Subkey: "SOFTWARE\Classes\ChangoEditor.js"; ValueType: string; ValueName: ""; ValueData: "JavaScript文件"; Flags: uninsdeletekey; Tasks: associate
Root: HKCU; Subkey: "SOFTWARE\Classes\ChangoEditor.js\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\ChangoEditor.exe,0"; Tasks: associate
Root: HKCU; Subkey: "SOFTWARE\Classes\ChangoEditor.js\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\ChangoEditor.exe"" ""%1"""; Tasks: associate

; 应用程序注册
Root: HKCU; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\ChangoEditor.exe"; ValueType: string; ValueName: ""; ValueData: "{app}\ChangoEditor.exe"; Flags: uninsdeletekey
Root: HKCU; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\ChangoEditor.exe"; ValueType: string; ValueName: "Path"; ValueData: "{app}"; Flags: uninsdeletekey

[Run]
; 安装完成后运行选项
Filename: "{app}\ChangoEditor.exe"; Description: "{cm:LaunchProgram,Chango Editor}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\examples"

[Code]
// 检查是否已安装旧版本
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
  Result := 0;
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;

