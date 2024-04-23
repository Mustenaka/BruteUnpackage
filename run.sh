# Set the relative path
relative_path="rarlib/libunrar.so"

# Get the absolute path
absolute_path="$(pwd)/$relative_path"

# Check if the file exists
if [ -f "$absolute_path" ]; then
    # Add the path to the user's .bashrc file
    echo "export UNRAR_LIB_PATH=$absolute_path" >> ~/.bashrc
    # Make the environment variable take effect immediately
    source ~/.bashrc
    echo "Successfully set UNRAR_LIB_PATH environment variable to: $absolute_path"
else
    echo "File $absolute_path does not exist. Please ensure the path is correct."
fi

# Run the Python script
python main.py "$@"
