# Set the relative path
$relative_path = "rarlib\libunrar.dll"

# Get the absolute path
$absolute_path = Join-Path -Path (Get-Location) -ChildPath $relative_path

# Check if the file exists
if (Test-Path $absolute_path) {
    # Add the path to the user's environment variables
    Add-Content -Path $PROFILE.AllUsersAllHosts -Value "Set-Item -Path env:UNRAR_LIB_PATH -Value \"$absolute_path\""
    # Make the environment variable take effect immediately
    . $PROFILE.AllUsersAllHosts
    Write-Output "Successfully set UNRAR_LIB_PATH environment variable to: $absolute_path"
} else {
    Write-Output "File $absolute_path does not exist. Please ensure the path is correct."
}

# Run the Python script
python main.py $args
