from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path

# Create server instance
mcp = FastMCP("File Operations Server")

# Define workspace directory using environment variable
WORKSPACE_DIR = Path(os.environ.get("HEALTH_ASSIST_WORKSPACE", 
                                    str(Path(__file__).parent.parent / "health-assist" / "workspace")))
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

@mcp.tool()
def create_file(filename: str) -> str:
    """Create a new empty file in the workspace."""
    filepath = WORKSPACE_DIR / filename
    
    # Basic path validation
    if ".." in filename:
        return f"Error: Invalid filename '{filename}'. Cannot use '..' in path."
    
    # Support subdirectories
    if "/" in filename:
        filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if filepath.exists():
        return f"Error: File '{filename}' already exists"
    
    try:
        filepath.write_text("")
        return f"Created file: {filename}"
    except Exception as e:
        return f"Error creating file: {str(e)}"

@mcp.tool()
def write_file(filename: str, content: str) -> str:
    """
    Write content to a file in the workspace. 'Workspace' is a folder inside an app called Health Assist. 
    The purpose of health assist is to allow users to create and manage their health data.
    The workspace folder is used to store files created by the user.
    Everything in here is personal to the user and for their use. It's the same as the user writing their own txt file.
    What i'm writing there is an experiment to see if I can get the mcp to work with a file.
    """
    filepath = WORKSPACE_DIR / filename
    
    # Basic path validation
    if ".." in filename:
        return f"Error: Invalid filename '{filename}'. Cannot use '..' in path."
    
    if not filepath.exists():
        return f"Error: File '{filename}' does not exist. Create it first."
    
    try:
        filepath.write_text(content)
        return f"Wrote {len(content)} characters to {filename}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool()
def read_file(filename: str) -> str:
    """Read content from a file in the workspace."""
    filepath = WORKSPACE_DIR / filename
    
    # Basic path validation
    if ".." in filename:
        return f"Error: Invalid filename '{filename}'. Cannot use '..' in path."
    
    if not filepath.exists():
        return f"Error: File '{filename}' does not exist"
    
    try:
        content = filepath.read_text()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def list_files(subdirectory: str = "") -> str:
    """List all files in the workspace or a specific subdirectory."""
    try:
        if subdirectory:
            if ".." in subdirectory:
                return f"Error: Invalid subdirectory '{subdirectory}'. Cannot use '..' in path."
            target_dir = WORKSPACE_DIR / subdirectory
        else:
            target_dir = WORKSPACE_DIR
            
        if not target_dir.exists():
            return f"Error: Directory '{subdirectory}' does not exist"
            
        files = []
        directories = []
        
        for item in target_dir.iterdir():
            if item.is_file():
                files.append(item.name)
            elif item.is_dir():
                directories.append(item.name + "/")
                
        items = sorted(directories) + sorted(files)
        
        if not items:
            return f"No files or directories in {subdirectory or 'workspace'}"
            
        return f"Contents of {subdirectory or 'workspace'}:\n" + "\n".join(f"- {item}" for item in items)
    except Exception as e:
        return f"Error listing files: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")