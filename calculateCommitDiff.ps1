#@author: Liquad Li on 2023-05-26
#$all = git diff c37bda72 b862a49d -- force-app
$commit1 = "c37bda72"
$commit2 = "a4e1097d"
$path = "force-app"
$pathClass = "force-app\main\default\classes"

$diffOutput = git diff --numstat $commit1 $commit2 -- $path
$sum = 0

foreach ($line in $diffOutput) {
    $fields = $line.Split()
    if ($fields.Length -ge 2) {
        if ($fields[0] -eq '-') {
            continue
        }
        $addedLines = [int]$fields[0]
        $deletedLines = [int]$fields[1]
        $sum += $addedLines + $deletedLines
    }
}

Write-Host "Total changed lines: $sum"

$diffOutput = git diff --numstat $commit1 $commit2 -- $pathClass
$sum = 0

foreach ($line in $diffOutput) {
    $fields = $line.Split()
    if ($fields.Length -ge 2) {
        if ($fields[0] -eq '-') {
            continue
        }
        $addedLines = [int]$fields[0]
        $deletedLines = [int]$fields[1]
        $sum += $addedLines + $deletedLines
    }
}

Write-Host "Total classes changed lines: $sum"

$diffOutput = git diff --name-only $commit1 $commit2
$fileCount = ($diffOutput | Measure-Object -Line).Lines

Write-Host "Total changed files: $fileCount"


