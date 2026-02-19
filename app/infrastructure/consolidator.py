import os

def consolidate_repo(output_file="CORE_LOGIC_CONSOLIDATED.txt"):
    ignore_dirs = {'.git', 'venv', '__pycache__', '.github', 'tests', 'build', 'dist'}
    allowed_extensions = {'.py', '.txt', '.json', '.md', '.env.example'}

    with open(output_file, "w", encoding="utf-8") as f:
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in allowed_extensions) and file != output_file:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, ".")
                    
                    f.write(f"\n\n--- INÍCIO: {relative_path} ---\n")
                    try:
                        with open(file_path, "r", encoding="utf-8") as content:
                            f.write(content.read())
                    except Exception as e:
                        f.write(f"ERRO AO LER ARQUIVO {relative_path}: {str(e)}")
                    f.write(f"\n--- FIM: {relative_path} ---\n")

if __name__ == "__main__":
    consolidate_repo()
