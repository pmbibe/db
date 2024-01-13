param(
    [string]$bpm="",
    [Parameter(Position=0,mandatory=$true)][string]$Module,
    [Parameter(Position=1)][string]$SubModule="",
    [Parameter(Position=2)][string]$Feature="",
    [string]$sourceDirectory = "D:\DS_IT_2537\app\Checklists\project_name\Checklist-2023\2023.12\2023.12.22",
    [string]$FileExtension ="*.sql"
)

$source = $sourceDirectory -replace "\\", "\\"
# Get a list of all files with the SQL extension
$files = Get-ChildItem -Path $sourceDirectory -Filter $FileExtension -Recurse
# Print the file names

function Get-Module-Name {
    param (
        $fileName
    )

    # $source = $sourceDirectory -replace "\\", "\\"
    $ModuleName = $fileName -replace "$source\\"
    return $ModuleName.Split('\')[0]

}

function Get-Sub-Module-Name {
    param (
        $fileName
    )

    # $source = $sourceDirectory -replace "\\", "\\"
    $ModuleName = $fileName -replace "$source\\"
    if ($ModuleName.Split('\').Length -gt 3){
        return $ModuleName.Split('\')[2]
    }
    return ""
}

function Get-Scripts {
    $Modules = @()
    $dict = @{ }
    $emptyDict = @{
        Rollback = @()
        Backup = @()
        Deploy = @()
    }

    foreach ($sqlScriptFile in $files.FullName) {
        $ModuleName = Get-Module-Name $sqlScriptFile
        if ($ModuleName -notIn $Modules) {
            $Modules += $ModuleName
            $dict[$ModuleName] = $emptyDict.Clone()
        }
        if ($subPath -eq "ROLLBACK") {
            $dict[$ModuleName]["Rollback"] += $sqlScriptFile -replace "$source\\$ModuleName\\"
        } elseif ($subPath -eq "BACKUP") {
            $dict[$ModuleName]["Backup"] += $sqlScriptFile -replace "$source\\$ModuleName\\"
        } else {
            $dict[$ModuleName]["Deploy"] += $sqlScriptFile -replace "$source\\$ModuleName\\"
        }           
    }

    $dict | ConvertTo-Json

}


function isIn {
    param(
        $a,
        $b
    )
    $rInput = '^\d+\..*'

    if (($a -match $rInput) -and ($b.ToUpper().Contains($a.ToUpper()))){
        return $true
    }
        
    return $false
}

function VerifyInput {
    param (
        $ModuleInput,
        $SubModuleInput,
        $FeatureInput,
        $scriptPath
    )
    $Module = Get-Module-Name($scriptPath)
    if (isIn $ModuleInput $Module){
        if ($SubModuleInput -ne "") {
            $SubModule = Get-Sub-Module-Name $scriptPath 
            if (-not (isIn $SubModuleInput $SubModule)){
                return $false
            }

        } elseif ($FeatureInput -ne "" -and (-not (isIn $SubModuleInput $scriptPath))) {
            return $false
        }
    } else {
        return $false
    }

    return $true

}

function Connect-Database {
    param (
        [string]$ServerName,
        [string]$DatabaseName,
        [int16]$Port,
        [string]$Username,
        [String]$Password,
        [string]$SQLPlusPath = "D:\Download\db-main\sqlplus\sqlplus.exe",
        [string]$SQLScriptName
    )

    & $SQLPlusPath ${Username}/${Password}@//${ServerName}:${Port}/${DatabaseName} "@${SQLScriptName}"
}

function ExcuteSQLScripts {
    param (
        $ModuleInput,
        $SubModuleInput,
        $FeatureInput
    )
    $IsExcute = $false
    foreach ($scriptPath in $files.FullName) {
        if (VerifyInput $ModuleInput $SubModuleInput $FeatureInput $scriptPath) {
            $IsExcute = $true
            
        }
    }    
    if (-not $IsExcute) {
        Write-Host "There is a bug in the input module, submodule, or feature that needs to be fixed before the system can function correctly."
    }

}

ExcuteSQLScripts $Module $SubModule $Feature

