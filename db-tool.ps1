param(
    [string]$bpm="",
    [Parameter(Position=0,mandatory=$true)][string]$Module,
    [Parameter(Position=1)][string]$SubModule="",
    [Parameter(Position=2)][string]$Feature="",
    [string]$sourceDirectory = "D:\DS_IT_2537\app\Checklists\project_name\Checklist-2023\2023.12\2023.12.22",
    [string]$FileExtension ="*.sql"
)

# Specify the file paths for success and error logs
$SuccessLogPath = 'success.log'
$ErrorLogPath = 'error.log'

# Execute SQL*Plus command and capture output
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

    # Build the SQL*Plus command
    & $SQLPlusPath ${Username}/${Password}@//${ServerName}:${Port}/${DatabaseName} "@${SQLScriptName}"
}

function Invoke-SqlplusScript {
    param(
        [string]$SqlplusCommand,
        [string]$SuccessLogPath,
        [string]$ErrorLogPath
    )

    # Execute SQL*Plus command and capture output
    $sqlplusOutput = Invoke-Expression -Command $SqlplusCommand 2>&1

    # Check if there are any errors in the SQL*Plus output
    if ($sqlplusOutput -match "ERROR") {
        # Log error messages
        $sqlplusOutput | Out-File -FilePath $ErrorLogPath -Append -Encoding utf8

        # Print error messages to console
        Write-Host "SQL*Plus script failed. Check $ErrorLogPath for details." -ForegroundColor Red

        # Exit with a non-zero code to mark the script as failed
        exit 1
    } else {
        # Log success messages
        $sqlplusOutput | Out-File -FilePath $SuccessLogPath -Append  -Encoding utf8

        # Print success messages to console
        Write-Host "SQL*Plus script executed successfully. Check $SuccessLogPath for details." -ForegroundColor Green

        # Exit with a zero code to indicate success
        exit 0
    }
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
            Invoke-SqlplusScript -SqlplusCommand $scriptPath -SuccessLogPath $SuccessLogPath -ErrorLogPath $ErrorLogPath
            $IsExcute = $true
            
        }
    }    
    if (-not $IsExcute) {
        Write-Host "There is a bug in the input module, submodule, or feature that needs to be fixed before the system can function correctly."
    }

}

ExcuteSQLScripts $Module $SubModule $Feature

