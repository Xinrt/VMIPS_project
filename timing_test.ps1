$pythonFile = "xt2191_tx701_timingsimulator.py"
$sourceFolder = "C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\conv_small"
$outputFolder = "C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\conv_small\output"

if (-not (Test-Path -Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder | Out-Null
}

$files = Get-ChildItem -Path $sourceFolder -Filter "Config*.txt"

foreach ($file in $files) {
    $configFile = Join-Path -Path $sourceFolder -ChildPath "Config.txt"
    $instructionLatencyFile = Join-Path -Path $sourceFolder -ChildPath "instruction_latency.txt"

    # Rename the config file
    Rename-Item -Path $file.FullName -NewName $configFile

    # Run the python script
    python $pythonFile --iodir $sourceFolder

    # Rename the output file
    $fileNumber = $file.Name.Replace("Config", "").Replace(".txt", "")
    $instructionLatencyOutput = Join-Path -Path $outputFolder -ChildPath ("instruction_latency" + $fileNumber + ".txt")
    Move-Item -Path $instructionLatencyFile -Destination $instructionLatencyOutput

    # Restore the config file name
    Rename-Item -Path $configFile -NewName $file.FullName
}
