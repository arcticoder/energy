# PowerShell script to find and remove copyright notices from all files

$targetDirectory = "C:\Users\echo_\Code\asciimath"
Set-Location $targetDirectory

Write-Host "Searching for files with copyright notices..." -ForegroundColor Green

# Find files that might contain copyright notices
$searchPatterns = @("copyright", "Copyright", "COPYRIGHT", "©", "(c)", "(C)")
$fileTypes = @("*.py", "*.md", "*.txt", "*.tex", "*.cpp", "*.h", "*.js")

$foundFiles = @()

foreach ($pattern in $searchPatterns) {
    foreach ($fileType in $fileTypes) {
        $files = Get-ChildItem -Recurse -Include $fileType | Where-Object { 
            (Get-Content $_.FullName -ErrorAction SilentlyContinue) -match $pattern 
        }
        $foundFiles += $files
    }
}

# Remove duplicates
$uniqueFiles = $foundFiles | Sort-Object FullName | Get-Unique -AsString

Write-Host "Found $($uniqueFiles.Count) files with potential copyright notices:" -ForegroundColor Yellow

foreach ($file in $uniqueFiles) {
    Write-Host "  $($file.FullName)" -ForegroundColor Cyan
    
    # Read file content
    $content = Get-Content $file.FullName -Raw
    
    # Remove various copyright patterns
    $updatedContent = $content -replace "Copyright.*?\d{4}.*?(\r?\n|$)", ""
    $updatedContent = $updatedContent -replace "copyright.*?\d{4}.*?(\r?\n|$)", ""
    $updatedContent = $updatedContent -replace "COPYRIGHT.*?\d{4}.*?(\r?\n|$)", ""
    $updatedContent = $updatedContent -replace "©.*?\d{4}.*?(\r?\n|$)", ""
    $updatedContent = $updatedContent -replace "\(c\).*?\d{4}.*?(\r?\n|$)", ""
    $updatedContent = $updatedContent -replace "\(C\).*?\d{4}.*?(\r?\n|$)", ""
    
    # Remove empty lines that might be left behind
    $updatedContent = $updatedContent -replace "(\r?\n){3,}", "`n`n"
    
    # Write back only if content changed
    if ($content -ne $updatedContent) {
        Set-Content -Path $file.FullName -Value $updatedContent.TrimEnd() -NoNewline
        Write-Host "    Removed copyright notices from $($file.Name)" -ForegroundColor Green
    } else {
        Write-Host "    No copyright changes needed in $($file.Name)" -ForegroundColor Gray
    }
}

Write-Host "Finished removing copyright notices." -ForegroundColor Green