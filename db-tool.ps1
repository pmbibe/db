param(
    [string]$BPM="", # BPM Number
    [Parameter(Position=0,mandatory=$true)][string]$Action = "list", # [ValidateSet('list','exec')]
    [Parameter(Position=1)][string]$Module="", # Module Name
    [Parameter(Position=2)][string]$SubModule="", # Sub Module Name
    [Parameter(Position=3)][string]$Feature="", # Feature Name
    [Parameter(mandatory=$true)][string]$ServerName, # Database Server
    [Parameter(mandatory=$true)][string]$DatabaseName, # Database Name
    [Parameter(mandatory=$true)][int16]$Port, # Database port
    [Parameter(mandatory=$true)]$Username, # Username
    [Parameter(mandatory=$true)][SecureString]$Password, # Password  
    [string]$SQLPlusPath = "D:\Download\db-main\sqlplus\sqlplus.exe",  
    [string]$sourceDirectory = "D:\DS_IT_2537\app\Checklists\project_name\Checklist-2023\2023.12\2023.12.22", # Checklist Path
    [string]$FileExtension ="*.sql"
)
function RunTool {
    # Specify the file paths for success and error logs
    $SuccessLogPath = 'success-$BPM.log'
    $ErrorLogPath = 'error-$BPM.log'

    # Get a list of all files with the SQL extension
    $files = Get-ChildItem -Path $sourceDirectory -Filter $FileExtension -Recurse

    
    $Password =  [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
    
    function Get-Module-Name {
        param (
            $fileName
        )

        $ModuleName = $fileName -replace [Regex]::Escape("$sourceDirectory")

        return $ModuleName.Split('\')[0]

    }

    function Get-Sub-Module-Name {
        param (
            $fileName
        )

        $ModuleName = $fileName -replace [Regex]::Escape("$sourceDirectory")
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
            
            $ScriptFile = $sqlScriptFile -replace [Regex]::Escape("$sourceDirectory$ModuleName\")
            
            if ($sqlScriptFile.ToUpper() -match "ROLLBACK") {
                $dict[$ModuleName]["Rollback"] += $ScriptFile 
            } elseif ($sqlScriptFile.ToUpper() -eq "BACKUP") {
                $dict[$ModuleName]["Backup"] += $ScriptFile 
            } else {
                $dict[$ModuleName]["Deploy"] += $ScriptFile 
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

    function Invoke-SqlplusScript {
        param(
            [string]$SuccessLogPath,
            [string]$ErrorLogPath,
            [string]$SQLScriptName        
        )

        # Execute SQL*Plus command and capture output
        $sqlplusOutput = & $SQLPlusPath "-L" ${Username}/${Password}@//${ServerName}:${Port}/${DatabaseName} "@${SQLScriptName}" 2>&1

        # Check if there are any errors in the SQL*Plus output
        if ($sqlplusOutput -match "logon denied") {

            Write-Host "Unable to connect to Oracle. Logon denied. Exiting SQL*Plus" -ForegroundColor Red

            Exit

        } elseif ($sqlplusOutput -match "ERROR") {
             
            # Log error messages
            $sqlplusOutput | Out-File -FilePath $ErrorLogPath -Encoding utf8 # -Append

            # Print error messages to console
            Write-Host "SQL*Plus script failed. Check $ErrorLogPath for details." -ForegroundColor Red

            Exit
        } else {
            # Log success messages
            Write-Host "Executing $SQLScriptName ..." -ForegroundColor Yellow
            $sqlplusOutput | Out-File -FilePath $SuccessLogPath -Encoding utf8 # -Append

            # Print success messages to console
            Write-Host "SQL*Plus script executed successfully. Check $SuccessLogPath for details." -ForegroundColor Green

        }
    }

    function ExcuteSQLScripts {
        param (
            $Module,
            $SubModule,
            $Feature
        )
        $IsExcute = $false
        foreach ($scriptPath in $files.FullName) {
            if (VerifyInput $Module $SubModule $Feature $scriptPath) {
                $IsExcute = $true
                Invoke-SqlplusScript -SuccessLogPath $SuccessLogPath -ErrorLogPath $ErrorLogPath -SQLScriptName $scriptPath
            }
        }    
        return $IsExcute
    }


    switch ($Action) {
        "list" {
            Get-Scripts
        }
        "exec" {
            if ($Module -eq "") {
                Write-Host "Specifies your Module" -ForegroundColor Red
            } else {
                $IsRun = ExcuteSQLScripts -Module $Module -SubModule $SubModule -Feature $Feature
                if (-not $IsRun) {
                    Write-Host "There is a bug in the input module, submodule, or feature that needs to be fixed before the system can function correctly." -ForegroundColor Red
                    Exit
                }
            }
        }
        default {
            Write-Host "Invalid Action: $Action" -ForegroundColor Red
        }
    }
}

RunTool
