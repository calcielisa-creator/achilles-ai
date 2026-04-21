import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_dir = os.path.commonpath([absolute_path, target_path]) == absolute_path
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_path]
        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=working_directory, capture_output=True, text= True, timeout=30)

        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        if result.stdout:
            output_parts.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output_parts.append(f"STDERR: {result.stderr}")
        if not result.stdout and not result.stderr:
            output_parts.append(f"No output produced")
        
        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
        
