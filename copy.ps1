# Path: test.ps1
param(
    [String]$FilePath
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$fileList = New-Object Collections.Specialized.StringCollection
$fileList.Add($FilePath)
[System.Windows.Forms.Clipboard]::SetFileDropList($fileList)
