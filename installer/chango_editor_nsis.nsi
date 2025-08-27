; Chango Editor NSIS 安装脚本
; 使用方法：makensis chango_editor_nsis.nsi

;--------------------------------
; 包含现代UI
!include "MUI2.nsh"
!include "FileFunc.nsh"

;--------------------------------
; 通用设置
Name "Chango Editor"
OutFile "..\dist\installer\ChangoEditor-Setup-NSIS-v1.0.0.exe"
Unicode True
RequestExecutionLevel user
InstallDir "$LOCALAPPDATA\Chango Editor"
InstallDirRegKey HKCU "Software\ChangoEditor" ""

; 版本信息
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "Chango Editor"
VIAddVersionKey "Comments" "功能强大的代码编辑器"
VIAddVersionKey "CompanyName" "Chango Team"
VIAddVersionKey "LegalCopyright" "© 2024 Chango Team"
VIAddVersionKey "FileDescription" "Chango Editor 安装程序"
VIAddVersionKey "FileVersion" "1.0.0.0"
VIAddVersionKey "ProductVersion" "1.0.0.0"

;--------------------------------
; 界面设置
!define MUI_ABORTWARNING
!define MUI_ICON "..\resources\icons\chango_editor.ico"
!define MUI_UNICON "..\resources\icons\chango_editor.ico"

; 欢迎页面
!define MUI_WELCOMEPAGE_TITLE "欢迎安装 Chango Editor"
!define MUI_WELCOMEPAGE_TEXT "这将在您的计算机上安装 Chango Editor v1.0.0。$\r$\n$\r$\nChango Editor 是一个功能强大的代码编辑器，提供类似 Sublime Text 的专业编辑体验。$\r$\n$\r$\n建议在安装前关闭所有其他应用程序。"

; 许可协议页面
!define MUI_LICENSEPAGE_TEXT_TOP "请阅读以下许可协议。"
!define MUI_LICENSEPAGE_TEXT_BOTTOM "如果您接受协议中的条款，请选择"我接受"继续安装。"

; 组件页面
!define MUI_COMPONENTSPAGE_SMALLDESC

; 安装目录页面
!define MUI_DIRECTORYPAGE_TEXT_TOP "安装程序将安装 Chango Editor 到以下目录。$\r$\n$\r$\n要安装到不同目录，请点击"浏览"按钮选择其他目录。"

; 安装进度页面
!define MUI_INSTFILESPAGE_FINISHHEADER_TEXT "安装完成"
!define MUI_INSTFILESPAGE_FINISHHEADER_SUBTEXT "Chango Editor 已成功安装。"

; 完成页面
!define MUI_FINISHPAGE_TITLE "Chango Editor 安装完成"
!define MUI_FINISHPAGE_TEXT "Chango Editor 已成功安装到您的计算机。$\r$\n$\r$\n点击"完成"关闭此向导。"
!define MUI_FINISHPAGE_RUN "$INSTDIR\ChangoEditor.exe"
!define MUI_FINISHPAGE_RUN_TEXT "运行 Chango Editor"
!define MUI_FINISHPAGE_LINK "访问 Chango Editor 项目主页"
!define MUI_FINISHPAGE_LINK_LOCATION "https://github.com/aweng1977/chango/chango-editor"

;--------------------------------
; 页面
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
; 语言
!insertmacro MUI_LANGUAGE "SimpChinese"

;--------------------------------
; 安装类型
InstType "完整安装"
InstType "最小安装"

;--------------------------------
; 组件
Section "核心程序 (必需)" SecCore
  SectionIn RO 1 2
  
  SetOutPath "$INSTDIR"
  File "..\dist\ChangoEditor.exe"
  File "..\LICENSE"
  File /oname=README.txt "..\README.md"
  
  ; 创建卸载程序
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; 注册表项
  WriteRegStr HKCU "Software\ChangoEditor" "" $INSTDIR
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChangoEditor" "DisplayName" "Chango Editor"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChangoEditor" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChangoEditor" "DisplayIcon" "$INSTDIR\ChangoEditor.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChangoEditor" "DisplayVersion" "1.0.0"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChangoEditor" "Publisher" "Chango Team"
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChangoEditor" "NoModify" 1
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChangoEditor" "NoRepair" 1
  
  ; 获取安装大小
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChangoEditor" "EstimatedSize" "$0"
SectionEnd

Section "桌面快捷方式" SecDesktop
  SectionIn 1
  CreateShortCut "$DESKTOP\Chango Editor.lnk" "$INSTDIR\ChangoEditor.exe"
SectionEnd

Section "开始菜单程序组" SecStartMenu
  SectionIn 1 2
  CreateDirectory "$SMPROGRAMS\Chango Editor"
  CreateShortCut "$SMPROGRAMS\Chango Editor\Chango Editor.lnk" "$INSTDIR\ChangoEditor.exe"
  CreateShortCut "$SMPROGRAMS\Chango Editor\卸载 Chango Editor.lnk" "$INSTDIR\Uninstall.exe"
  CreateShortCut "$SMPROGRAMS\Chango Editor\使用说明.lnk" "$INSTDIR\README.txt"
SectionEnd

Section "示例文件" SecExamples
  SectionIn 1
  SetOutPath "$INSTDIR\examples"
  File /r "..\test_files\*.*"
  CreateShortCut "$SMPROGRAMS\Chango Editor\示例文件.lnk" "$INSTDIR\examples"
SectionEnd

Section "文件关联" SecAssoc
  SectionIn 1
  
  ; Python 文件关联
  WriteRegStr HKCU "SOFTWARE\Classes\.py\OpenWithProgids" "ChangoEditor.py" ""
  WriteRegStr HKCU "SOFTWARE\Classes\ChangoEditor.py" "" "Python文件"
  WriteRegStr HKCU "SOFTWARE\Classes\ChangoEditor.py\DefaultIcon" "" "$INSTDIR\ChangoEditor.exe,0"
  WriteRegStr HKCU "SOFTWARE\Classes\ChangoEditor.py\shell\open\command" "" '"$INSTDIR\ChangoEditor.exe" "%1"'
  
  ; JavaScript 文件关联
  WriteRegStr HKCU "SOFTWARE\Classes\.js\OpenWithProgids" "ChangoEditor.js" ""
  WriteRegStr HKCU "SOFTWARE\Classes\ChangoEditor.js" "" "JavaScript文件"
  WriteRegStr HKCU "SOFTWARE\Classes\ChangoEditor.js\DefaultIcon" "" "$INSTDIR\ChangoEditor.exe,0"
  WriteRegStr HKCU "SOFTWARE\Classes\ChangoEditor.js\shell\open\command" "" '"$INSTDIR\ChangoEditor.exe" "%1"'
  
  ; 添加到应用程序路径
  WriteRegStr HKCU "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\ChangoEditor.exe" "" "$INSTDIR\ChangoEditor.exe"
  WriteRegStr HKCU "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\ChangoEditor.exe" "Path" "$INSTDIR"
SectionEnd

;--------------------------------
; 组件描述
LangString DESC_SecCore ${LANG_SIMPCHINESE} "Chango Editor 核心程序文件（必需）"
LangString DESC_SecDesktop ${LANG_SIMPCHINESE} "在桌面创建 Chango Editor 快捷方式"
LangString DESC_SecStartMenu ${LANG_SIMPCHINESE} "在开始菜单创建 Chango Editor 程序组"
LangString DESC_SecExamples ${LANG_SIMPCHINESE} "安装示例代码文件，帮助您快速了解编辑器功能"
LangString DESC_SecAssoc ${LANG_SIMPCHINESE} "关联常用代码文件格式（.py, .js 等）到 Chango Editor"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecCore} $(DESC_SecCore)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecExamples} $(DESC_SecExamples)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecAssoc} $(DESC_SecAssoc)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
; 卸载程序
Section "Uninstall"
  ; 删除文件
  Delete "$INSTDIR\ChangoEditor.exe"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\README.txt"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir /r "$INSTDIR\examples"
  RMDir "$INSTDIR"
  
  ; 删除快捷方式
  Delete "$DESKTOP\Chango Editor.lnk"
  RMDir /r "$SMPROGRAMS\Chango Editor"
  
  ; 删除注册表项
  DeleteRegKey HKCU "Software\ChangoEditor"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ChangoEditor"
  
  ; 删除文件关联
  DeleteRegKey HKCU "SOFTWARE\Classes\ChangoEditor.py"
  DeleteRegKey HKCU "SOFTWARE\Classes\ChangoEditor.js"
  DeleteRegValue HKCU "SOFTWARE\Classes\.py\OpenWithProgids" "ChangoEditor.py"
  DeleteRegValue HKCU "SOFTWARE\Classes\.js\OpenWithProgids" "ChangoEditor.js"
  DeleteRegKey HKCU "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\ChangoEditor.exe"
SectionEnd

