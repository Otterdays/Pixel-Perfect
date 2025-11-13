<# Reliable Codebase Audit Script for Pixel Perfect
Counts non-blank, non-comment lines across all Python files recursively
Outputs summary report to audit_results.txt #>

$projectRoot = 'c:\Users\Ry\Desktop\Pixel-Perfect'
$outputFile = Join-Path $projectRoot 'audit_results.txt'
$totalLines = 0
$fileCount = 0

# Clear previous results
if (Test-Path $outputFile) { Remove-Item $outputFile -Force }

# Recursively process all .py files
Get-ChildItem -Path $projectRoot -Filter '*.py' -Recurse | ForEach-Object {
    $filePath = $_.FullName
    $fileCount++
    $fileLines = 0
    $inBlockComment = $false

    # Read file line by line
    Get-Content $filePath | ForEach-Object {
        $line = $_.Trim()

        # Handle block comments (""" ... """)
        if ($line -match '"""') {
            $inBlockComment = -not $inBlockComment
            return
        }
        if ($inBlockComment) { return }

        # Skip line comments and blank lines
        if ($line -match '^#' -or $line -eq '') { return }

        $fileLines++
        $totalLines++
    }

    # Write file-specific results
    Add-Content $outputFile "File: $filePath"
    Add-Content $outputFile "Non-blank, non-comment lines: $fileLines`n"
}

# Write summary
Add-Content $outputFile "=== Audit Summary ==="
Add-Content $outputFile "Total Python files processed: $fileCount"
Add-Content $outputFile "Total non-blank, non-comment lines: $totalLines"
Add-Content $outputFile "Audit completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

Write-Host "Audit completed. Results saved to $outputFile"