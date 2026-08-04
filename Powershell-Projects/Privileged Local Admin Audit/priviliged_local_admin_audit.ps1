# Goal: Identify members of the local Administrators group and export a report

param(
    [string]$outputPath = (Join-Path $PSScriptRoot "Outputs\report.csv")
)

# setup save location
$outputFolder = Split-Path $OutputPath -Parent
try {
    if (-not (Test-Path $outputFolder)) {
        New-Item -Path $outputFolder -ItemType Directory -ErrorAction Stop | Out-Null 
    }
} 
catch {
    Write-Warning "The directory could not be created: $($_.Exception.Message)"
    return
}

# collect admin group members
try {
    $localAdminGroupMembership = Get-LocalGroupMember -Group "Administrators" | 
    Select-Object @{
        Name = "ComputerName"
        Expression = { $env:COMPUTERNAME }
    }, 
    @{
        Name = "AccountName"
        Expression = { $_.Name }
    }, ObjectClass, PrincipalSource, SID -ErrorAction Stop
}
catch {
    Write-Warning "The members could not be collected: $($_.Exception.Message)"
    return
}



# export to csv
$localAdminGroupMembership | Export-csv -Path $outputPath -NoTypeInformation

    
$localAdminGroupMembership | Format-List 