# Specify the path to the blender.exe
$blenderPath = "C:\Program Files\Blender Foundation\Blender 3.5\blender.exe"

# Get the current script directory
$scriptDirectory = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Construct the path to the python script
# $pythonScriptPath = Join-Path -Path $scriptDirectory -ChildPath "blender_test.py"
$pythonScriptPath = Join-Path -Path $scriptDirectory -ChildPath "flash_test_2.py"

# Run Blender with the python script
& $blenderPath --background --python $pythonScriptPath
