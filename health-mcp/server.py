from mcp.server.fastmcp import FastMCP
import json
import os
from pathlib import Path
from datetime import datetime
import uuid
from typing import Dict, List, Optional
import jsonschema
from dateutil import parser as date_parser

# Create server instance
mcp = FastMCP("Health Narrative Server")

# Define workspace directory
WORKSPACE_DIR = Path(os.environ.get("HEALTH_ASSIST_WORKSPACE", 
                                    str(Path(__file__).parent.parent / "workspace")))

# Load schema
with open(Path(__file__).parent / "schema.json", "r") as f:
    HEALTH_EVENT_SCHEMA = json.load(f)

# Ensure subdirectories exist
(WORKSPACE_DIR / "narratives").mkdir(parents=True, exist_ok=True)
(WORKSPACE_DIR / "structured").mkdir(parents=True, exist_ok=True)
(WORKSPACE_DIR / "conversations").mkdir(parents=True, exist_ok=True)

@mcp.tool()
def save_health_event(
    user_id: str,
    narrative: str,
    structured_data: str,
    event_type: str,
    event_date: Optional[str] = None,
    confidence_level: str = "certain"
) -> str:
    """
    Save a health event with both narrative and structured data.
    
    Args:
        user_id: User identifier (e.g., 'bob')
        narrative: User's description in their own words
        structured_data: JSON string of extracted structured information
        event_type: Type of event (doctor_visit, symptom, etc.)
        event_date: Date of event (YYYY-MM-DD), defaults to today
        confidence_level: AI's confidence in extracted data
    """
    try:
        # Parse structured data
        structured = json.loads(structured_data) if structured_data else {}
        
        # Create event
        event = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "date": event_date or datetime.now().strftime("%Y-%m-%d"),
            "type": event_type,
            "narrative": narrative,
            "structured": structured,
            "confidence_level": confidence_level,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Validate against schema
        jsonschema.validate(event, HEALTH_EVENT_SCHEMA)
        
        # Save structured data
        structured_file = WORKSPACE_DIR / "structured" / f"{user_id}_events.json"
        events = []
        if structured_file.exists():
            with open(structured_file, "r") as f:
                events = json.load(f)
        events.append(event)
        with open(structured_file, "w") as f:
            json.dump(events, f, indent=2, default=str)
        
        # Update narrative
        narrative_file = WORKSPACE_DIR / "narratives" / f"{user_id}_narrative.md"
        with open(narrative_file, "a") as f:
            if narrative_file.exists() and narrative_file.stat().st_size > 0:
                f.write("\n\n")
            f.write(f"## {event['date']} - {event_type.replace('_', ' ').title()}\n\n")
            f.write(f"{narrative}\n")
        
        return f"Saved health event: {event['id']}"
    except Exception as e:
        return f"Error saving health event: {str(e)}"

@mcp.tool()
def get_health_narrative(user_id: str) -> str:
    """Get the complete health narrative for a user."""
    narrative_file = WORKSPACE_DIR / "narratives" / f"{user_id}_narrative.md"
    
    if not narrative_file.exists():
        return f"No health narrative found for user: {user_id}"
    
    try:
        with open(narrative_file, "r") as f:
            content = f.read()
        return content if content else "Health narrative is empty"
    except Exception as e:
        return f"Error reading health narrative: {str(e)}"

@mcp.tool()
def get_recent_events(user_id: str, limit: int = 5) -> str:
    """Get the most recent health events for a user."""
    structured_file = WORKSPACE_DIR / "structured" / f"{user_id}_events.json"
    
    if not structured_file.exists():
        return f"No health events found for user: {user_id}"
    
    try:
        with open(structured_file, "r") as f:
            events = json.load(f)
        
        # Sort by date (most recent first)
        events.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # Get recent events
        recent = events[:limit]
        
        # Format for display
        result = f"Recent health events for {user_id}:\n\n"
        for event in recent:
            result += f"**{event['date']}** - {event['type'].replace('_', ' ').title()}\n"
            result += f"{event['narrative']}\n\n"
        
        return result
    except Exception as e:
        return f"Error reading health events: {str(e)}"

@mcp.tool()
def search_events(
    user_id: str,
    query: str,
    event_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """
    Search health events by keyword, type, or date range.
    
    Args:
        user_id: User identifier
        query: Text to search for in narratives and structured data
        event_type: Filter by event type
        start_date: Filter events after this date (YYYY-MM-DD)
        end_date: Filter events before this date (YYYY-MM-DD)
    """
    structured_file = WORKSPACE_DIR / "structured" / f"{user_id}_events.json"
    
    if not structured_file.exists():
        return f"No health events found for user: {user_id}"
    
    try:
        with open(structured_file, "r") as f:
            events = json.load(f)
        
        # Filter events
        filtered = []
        query_lower = query.lower()
        
        for event in events:
            # Check text match
            if query_lower not in event['narrative'].lower():
                # Also check structured data
                if query_lower not in json.dumps(event.get('structured', {})).lower():
                    continue
            
            # Check event type
            if event_type and event['type'] != event_type:
                continue
            
            # Check date range
            event_date = event.get('date', '')
            if start_date and event_date < start_date:
                continue
            if end_date and event_date > end_date:
                continue
            
            filtered.append(event)
        
        # Sort by date
        filtered.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # Format results
        if not filtered:
            return f"No matching events found for '{query}'"
        
        result = f"Found {len(filtered)} matching events:\n\n"
        for event in filtered:
            result += f"**{event['date']}** - {event['type'].replace('_', ' ').title()}\n"
            result += f"{event['narrative']}\n\n"
        
        return result
    except Exception as e:
        return f"Error searching health events: {str(e)}"

@mcp.tool()
def extract_health_info(narrative: str) -> str:
    """
    Extract structured health information from a narrative.
    Returns JSON with identified medications, symptoms, diagnoses, etc.
    
    Note: This is a placeholder - in a real implementation, this would use
    NLP or Claude's capabilities to extract structured data.
    """
    # This is a simplified example - you would typically use Claude's
    # understanding to extract this information
    
    extracted = {
        "symptoms": [],
        "diagnoses": [],
        "medications": [],
        "test_results": [],
        "recommendations": []
    }
    
    # Simple keyword extraction (placeholder)
    narrative_lower = narrative.lower()
    
    # Look for common patterns
    if "cholesterol" in narrative_lower:
        if "high" in narrative_lower:
            extracted["diagnoses"].append("high cholesterol")
    
    if "statin" in narrative_lower or "atorvastatin" in narrative_lower:
        extracted["medications"].append({
            "name": "atorvastatin",
            "status": "started"
        })
    
    if "walk" in narrative_lower and ("more" in narrative_lower or "exercise" in narrative_lower):
        extracted["recommendations"].append("increase walking/exercise")
    
    return json.dumps(extracted, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")