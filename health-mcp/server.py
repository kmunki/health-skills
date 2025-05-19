from mcp.server.fastmcp import FastMCP
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List

# Create server instance
mcp = FastMCP("Health Narrative Server")

# Define workspace directory
WORKSPACE_DIR = Path(os.environ.get("HEALTH_ASSIST_WORKSPACE", 
                                    str(Path(__file__).parent.parent / "workspace")))

def create_filename(topic: str, date: str) -> str:
    """Create a human-readable filename from topic and date"""
    # Clean the topic to be filename-safe
    safe_topic = topic.lower().replace(" ", "-").replace("_", "-")
    safe_topic = "".join(c for c in safe_topic if c.isalnum() or c == "-")
    return f"{date}-{safe_topic}"

def ensure_user_dirs(user_id: str):
    """Ensure user directories exist"""
    (WORKSPACE_DIR / "narratives" / user_id).mkdir(parents=True, exist_ok=True)
    (WORKSPACE_DIR / "structured" / user_id).mkdir(parents=True, exist_ok=True)

@mcp.tool()
def save_health_note(
    user_id: str,
    topic: str,
    narrative: str,
    date: Optional[str] = None,
    extract_structure: bool = True
) -> str:
    """
    Save a health note with human-readable naming.
    
    Args:
        user_id: User identifier (e.g., 'kyle')
        topic: Brief description (e.g., 'gas-issues', 'supplements-update')
        narrative: User's description in their own words
        date: Optional date (YYYY-MM-DD), defaults to today
        extract_structure: Whether to create a structured JSON file
    """
    try:
        ensure_user_dirs(user_id)
        date_str = date or datetime.now().strftime("%Y-%m-%d")
        filename = create_filename(topic, date_str)
        
        # Save narrative
        narrative_path = WORKSPACE_DIR / "narratives" / user_id / f"{filename}.md"
        with open(narrative_path, "w") as f:
            f.write(f"# {topic.replace('-', ' ').title()} - {date_str}\n\n")
            f.write(narrative)
        
        # Save basic structure
        if extract_structure:
            structure = {
                "date": date_str,
                "topic": topic,
                "narrative": narrative,
                "extracted_info": {}  # Claude can fill this via update_health_note
            }
            
            json_path = WORKSPACE_DIR / "structured" / user_id / f"{filename}.json"
            with open(json_path, "w") as f:
                json.dump(structure, f, indent=2)
        
        return f"Saved health note: {filename}"
    except Exception as e:
        return f"Error saving health note: {str(e)}"

@mcp.tool()
def read_health_notes(
    user_id: str,
    days_back: Optional[int] = 30,
    topic_filter: Optional[str] = None
) -> str:
    """
    Read recent health notes for a user.
    
    Args:
        user_id: User identifier
        days_back: How many days of history to read (default 30)
        topic_filter: Optional topic to filter by (e.g., 'supplements')
    """
    try:
        narratives_dir = WORKSPACE_DIR / "narratives" / user_id
        structured_dir = WORKSPACE_DIR / "structured" / user_id
        
        if not narratives_dir.exists():
            return f"No health notes found for user: {user_id}"
        
        # Get all files from the last N days
        cutoff_date = datetime.now() - timedelta(days=days_back)
        notes = []
        
        for narrative_file in sorted(narratives_dir.glob("*.md"), reverse=True):
            # Parse date from filename (YYYY-MM-DD-topic.md)
            try:
                file_date = datetime.strptime(narrative_file.stem[:10], "%Y-%m-%d")
                if file_date < cutoff_date:
                    continue
                    
                # Apply topic filter if provided
                if topic_filter:
                    file_topic = narrative_file.stem[11:]  # Everything after date
                    if topic_filter.lower() not in file_topic.lower():
                        continue
                
                # Read narrative
                with open(narrative_file, "r") as f:
                    narrative_content = f.read()
                
                # Read structured data if it exists
                json_file = structured_dir / f"{narrative_file.stem}.json"
                structured_data = {}
                if json_file.exists():
                    with open(json_file, "r") as f:
                        structured_data = json.load(f)
                
                notes.append({
                    "filename": narrative_file.stem,
                    "date": file_date.strftime("%Y-%m-%d"),
                    "narrative": narrative_content,
                    "structured": structured_data
                })
                
            except ValueError:
                # Skip files that don't match our naming pattern
                continue
        
        if not notes:
            return f"No health notes found in the last {days_back} days"
        
        # Format results
        result = f"Health notes for {user_id} (last {days_back} days):\n\n"
        for note in notes:
            result += f"=== {note['filename']} ===\n"
            result += note['narrative']
            if note['structured'] and note['structured'].get('extracted_info'):
                result += f"\n\nExtracted Info:\n{json.dumps(note['structured']['extracted_info'], indent=2)}"
            result += "\n\n"
        
        return result
    except Exception as e:
        return f"Error reading health notes: {str(e)}"

@mcp.tool()
def update_health_note(
    user_id: str,
    filename: str,
    extracted_info: Dict
) -> str:
    """
    Update the structured data for a health note.
    
    Args:
        user_id: User identifier
        filename: The filename (e.g., '2025-01-19-gas-issues')
        extracted_info: Dictionary of extracted health information
    """
    try:
        json_path = WORKSPACE_DIR / "structured" / user_id / f"{filename}.json"
        
        if not json_path.exists():
            return f"No structured file found: {filename}"
        
        # Read existing structure
        with open(json_path, "r") as f:
            structure = json.load(f)
        
        # Update extracted info
        structure['extracted_info'] = extracted_info
        structure['updated_at'] = datetime.now().isoformat()
        
        # Save updated structure
        with open(json_path, "w") as f:
            json.dump(structure, f, indent=2)
        
        return f"Updated structured data for: {filename}"
    except Exception as e:
        return f"Error updating health note: {str(e)}"

@mcp.tool()
def find_health_topics(user_id: str) -> str:
    """
    List all health topics that have been discussed.
    
    Args:
        user_id: User identifier
    """
    try:
        narratives_dir = WORKSPACE_DIR / "narratives" / user_id
        
        if not narratives_dir.exists():
            return f"No health notes found for user: {user_id}"
        
        topics = set()
        dates_by_topic = {}
        
        for narrative_file in narratives_dir.glob("*.md"):
            try:
                # Extract topic from filename (YYYY-MM-DD-topic.md)
                parts = narrative_file.stem.split("-", 3)
                if len(parts) >= 4:
                    topic = parts[3]
                    date = "-".join(parts[:3])
                    
                    topics.add(topic)
                    if topic not in dates_by_topic:
                        dates_by_topic[topic] = []
                    dates_by_topic[topic].append(date)
            except:
                continue
        
        if not topics:
            return "No topics found"
        
        # Format results
        result = f"Health topics for {user_id}:\n\n"
        for topic in sorted(topics):
            dates = sorted(dates_by_topic[topic], reverse=True)
            result += f"**{topic.replace('-', ' ').title()}**\n"
            result += f"  Discussed on: {', '.join(dates[:5])}"
            if len(dates) > 5:
                result += f" ... ({len(dates)} total)"
            result += "\n\n"
        
        return result
    except Exception as e:
        return f"Error finding health topics: {str(e)}"

@mcp.tool()
def get_health_note(
    user_id: str,
    filename: str
) -> str:
    """
    Get a specific health note by filename.
    
    Args:
        user_id: User identifier
        filename: The filename (e.g., '2025-01-19-gas-issues')
    """
    try:
        narrative_path = WORKSPACE_DIR / "narratives" / user_id / f"{filename}.md"
        json_path = WORKSPACE_DIR / "structured" / user_id / f"{filename}.json"
        
        if not narrative_path.exists():
            return f"Health note not found: {filename}"
        
        # Read narrative
        with open(narrative_path, "r") as f:
            narrative = f.read()
        
        # Read structured data if it exists
        structured = {}
        if json_path.exists():
            with open(json_path, "r") as f:
                structured = json.load(f)
        
        result = f"=== {filename} ===\n\n"
        result += narrative
        
        if structured and structured.get('extracted_info'):
            result += f"\n\nExtracted Info:\n{json.dumps(structured['extracted_info'], indent=2)}"
        
        return result
    except Exception as e:
        return f"Error reading health note: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")