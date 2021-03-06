# Auto-generated by EclipseNSIS Script Wizard
# 19-mar-2009 2:56:12

Name "Avrak "

RequestExecutionLevel admin
SetCompressor zlib
SetCompressionLevel 0
 

# General Symbol Definitions
!define REGKEY "SOFTWARE\$(^Name)"
!define VERSION 1.0
!define COMPANY "Nahuel Defoss�"
!define URL ""

!define MYSQL_DIR "E:\mysql-5.1.31-win32"
!define QT_DIR "E:\Qt\4.4.3"
!define PYTHON_DIR "C:\python25"

# MUI Symbol Definitions
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install-colorful.ico"
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_STARTMENUPAGE_REGISTRY_ROOT HKLM

!define MUI_STARTMENUPAGE_NODISABLE
!define MUI_STARTMENUPAGE_REGISTRY_KEY ${REGKEY}
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME StartMenuGroup
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "Avrak "
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall-colorful.ico"

# Included files
!include Sections.nsh
!include MUI2.nsh

# Variables
Var StartMenuGroup

# Installer pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE ..\..\doc\license.txt
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuGroup
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

# Installer languages
!insertmacro MUI_LANGUAGE SpanishInternational

# Installer attributes
OutFile "..\..\Avrak Setup.exe"
InstallDir $PROGRAMFILES\Avrak
CRCCheck on
XPStyle on
ShowInstDetails show
VIProductVersion 1.0.0.0
VIAddVersionKey ProductName "Avrak "
VIAddVersionKey ProductVersion "${VERSION}"
VIAddVersionKey CompanyName "${COMPANY}"
VIAddVersionKey FileVersion "${VERSION}"
VIAddVersionKey FileDescription ""
VIAddVersionKey LegalCopyright ""
InstallDirRegKey HKLM "${REGKEY}" Path
ShowUninstDetails show

# Installer sections
Section -Main SEC0000
    SetOutPath $INSTDIR
    SetOverwrite on
    # Copiamos el generado de PyInstaller
    File /a /r "..\..\pyscada\distmain_gui\*"
    
    # Los plugins de la DB deben ir en una subcarpeta
    CreateDirectory $INSTDIR\sqldrivers
    SetOutPath $INSTDIR\sqldrivers
    # Copiamos plugins de MySQL
    File /a /r "${QT_DIR}\plugins\sqldrivers\*.dll"
    
    # Ahora la DB
    SetOutPath $INSTDIR
    # Copiamos el SQL
    File "..\sql\creacion.sql"
        
    # Copiar la configuracion de MySQL
    File "${MYSQL_DIR}\my-medium.ini"  
    Rename "$INSTDIR\my-medium.ini" "$INSTDIR\my.ini"
    
    CreateDirectory $INSTDIR\bin
    SetOutPath $INSTDIR\bin
    File /a /r "${MYSQL_DIR}\bin\mysqld.exe"
    File /a /r "${MYSQL_DIR}\bin\mysql.exe"
    CreateDirectory $INSTDIR\data
    SetOutPath $INSTDIR\data
    File /a /r "${MYSQL_DIR}\original\data\*"
    CreateDirectory $INSTDIR\share
    SetOutPath $INSTDIR\share
    File /a /r "${MYSQL_DIR}\share\*"
    # Copiamos el archivo de instalacion
    
    WriteRegStr HKLM "${REGKEY}\Components" Main 1
SectionEnd


# Postinstalacion
Section -post SEC0001
    WriteRegStr HKLM "${REGKEY}" Path $INSTDIR
    SetOutPath $INSTDIR
    Exec "$INSTDIR\cfg_setup.exe -l creacion.sql"
    
    WriteUninstaller $INSTDIR\uninstall.exe
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    SetOutPath $SMPROGRAMS\$StartMenuGroup
    CreateShortcut "$SMPROGRAMS\$StartMenuGroup\$(^Name).lnk" $INSTDIR\avrak.exe
    CreateDirectory "$SMPROGRAMS\$StartMenuGroup\Avanzado"
    CreateShortcut "$SMPROGRAMS\$StartMenuGroup\Avanzado\$(^Name) Depuraci�n.lnk" $INSTDIR\avrak_dbg.exe
    
    CreateShortcut "$SMPROGRAMS\$StartMenuGroup\Desinstalar $(^Name).lnk" $INSTDIR\uninstall.exe
    !insertmacro MUI_STARTMENU_WRITE_END
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayName "$(^Name)"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayVersion "${VERSION}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" Publisher "${COMPANY}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayIcon $INSTDIR\uninstall.exe
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" UninstallString $INSTDIR\uninstall.exe
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" NoModify 1
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" NoRepair 1
SectionEnd

# Macro for selecting uninstaller sections
!macro SELECT_UNSECTION SECTION_NAME UNSECTION_ID
    Push $R0
    ReadRegStr $R0 HKLM "${REGKEY}\Components" "${SECTION_NAME}"
    StrCmp $R0 1 0 next${UNSECTION_ID}
    !insertmacro SelectSection "${UNSECTION_ID}"
    GoTo done${UNSECTION_ID}
next${UNSECTION_ID}:
    !insertmacro UnselectSection "${UNSECTION_ID}"
done${UNSECTION_ID}:
    Pop $R0
!macroend

# Uninstaller sections
Section /o -un.Main UNSEC0000
    RmDir /r /REBOOTOK $INSTDIR
    DeleteRegValue HKLM "${REGKEY}\Components" Main
SectionEnd

Section -un.post UNSEC0001
    DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)"
    #Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\Uninstall $(^Name).lnk"
    # Quitar las entradas del men� inicio
    #Exec "$INSTDIR\cfg_setup.exe -u"
    ExecWait "net stop mysql_avrak"
    ExecWait "$INSTDIR\bin\mysqld.exe --uninstall"
    
    Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\$(^Name).lnk"
    Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\Desinstalar $(^Name).lnk"
    Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\Avanzado\$(^Name) Depuraci�n.lnk"
    Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\Avanzado"
    
    Delete /REBOOTOK $INSTDIR\uninstall.exe
    DeleteRegValue HKLM "${REGKEY}" StartMenuGroup
    DeleteRegValue HKLM "${REGKEY}" Path
    DeleteRegKey /IfEmpty HKLM "${REGKEY}\Components"
    DeleteRegKey /IfEmpty HKLM "${REGKEY}"
    RmDir /REBOOTOK $SMPROGRAMS\$StartMenuGroup
    RmDir /REBOOTOK $INSTDIR
SectionEnd

# Installer functions
Function .onInit
    InitPluginsDir
    ; Leemos si hay un desinstalador...
    ReadRegStr $R0 HKLM \
        "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" \
        "UninstallString"
    StrCmp $R0 "" done
 
    MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
       "Avrak ya est� instalado. $\n$\nDesinstalar la version previa?"\
    IDOK uninst
    Abort
 
;Run the uninstaller
uninst:
  ClearErrors
  ExecWait '$R0 _?=$INSTDIR' ;Do not copy the uninstaller to a temp file
 
  IfErrors no_remove_uninstaller
    ;You can either use Delete /REBOOTOK in the uninstaller or add some code
    ;here to remove the uninstaller. Use a registry key to check
    ;whether the user has chosen to uninstall. If you are using an uninstaller
    ;components page, make sure all sections are uninstalled.
  no_remove_uninstaller:
 
done:
   
FunctionEnd

# Uninstaller functions
Function un.onInit
    SetAutoClose true
    ReadRegStr $INSTDIR HKLM "${REGKEY}" Path
    !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuGroup
    !insertmacro SELECT_UNSECTION Main ${UNSEC0000}
FunctionEnd

