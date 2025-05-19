from mcp.server.fastmcp import FastMCP
import json
import os
from pathlib import Path
from datetime import datetime
import uuid
from typing import Dict, List, Optional
from dateutil import parser as date_parser

# Create server instance
mcp = FastMCP("Health Narrative Server")

# Define workspace directory
WORKSPACE_DIR = Path(os.environ.get("HEALTH_ASSIST_WORKSPACE", 
                                    str(Path(__file__).parent.parent / "workspace")))

# Ensure subdirectories exist
(WORKSPACE_DIR / "narratives").mkdir(parents=True, exist_ok=True)
(WORKSPACE_DIR / "structured").mkdir(parents=True, exist_ok=True)
(WORKSPACE_DIR / "conversations").mkdir(parents=True, exist_ok=True)

@mcp.tool()
def record_health_narrative(
    user_id: str,
    narrative: str,
    event_type: Optional[str] = None,
    event_date: Optional[str] = None
) -> str:
    """
    Record a health narrative from the user's natural conversation.
    
    Args:
        user_id: User identifier (e.g., 'bob')
        narrative: User's description in their own words
        event_type: Optional type of event (any string allowed)
        event_date: Optional date (YYYY-MM-DD), defaults to today
    """
    try:
        # Create event
        event = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "date": event_date or datetime.now().strftime("%Y-%m-%d"),
            "type": event_type or "health_note",
            "narrative": narrative,
            "structured": {},  # Empty for now, can be filled later
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save structured data
        structured_file = WORKSPACE_DIR / "structured" / f"{user_id}_events.json"
        events = []
        if structured_file.exists():
            with open(structured_file, "r") as f:
                events = json.load(f)
        events.append(event)
        with open(structured_file, "w") as f:
            json.dump(events, f, indent=2, default=str)
        
        # Update narrative file
        narrative_file = WORKSPACE_DIR / "narratives" / f"{user_id}_narrative.md"
        with open(narrative_file, "a") as f:
            if narrative_file.exists() and narrative_file.stat().st_size > 0:
                f.write("\n\n")
            title = event_type.replace('_', ' ').title() if event_type else "Health Note"
            f.write(f"## {event['date']} - {title}\n\n")
            f.write(f"{narrative}\n")
        
        return f"Recorded health narrative (ID: {event['id'][:8]}...)"
    except Exception as e:
        return f"Error recording health narrative: {str(e)}"

@mcp.tool()
def update_event_structure(
    event_id: str,
    user_id: str,
    structured_data: Dict
) -> str:
    """
    Update the structured data for an existing health event.
    This is typically called after AI extracts information from the narrative.
    
    Args:
        event_id: ID of the event to update
        user_id: User identifier
        structured_data: Dictionary of extracted health information
    """
    try:
        structured_file = WORKSPACE_DIR / "structured" / f"{user_id}_events.json"
        
        if not structured_file.exists():
            return f"No events found for user: {user_id}"
        
        with open(structured_file, "r") as f:
            events = json.load(f)
        
        # Find and update the event
        updated = False
        for event in events:
            if event['id'] == event_id:
                event['structured'] = structured_data
                event['updated_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if not updated:
            return f"Event not found: {event_id}"
        
        # Save updated events
        with open(structured_file, "w") as f:
            json.dump(events, f, indent=2, default=str)
        
        return f"Updated structured data for event: {event_id[:8]}..."
    except Exception as e:
        return f"Error updating event structure: {str(e)}"

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
            result += f"{event['narrative']}\n"
            if event.get('structured'):
                result += f"*Extracted info:* {json.dumps(event['structured'], indent=2)}\n"
            result += "\n"
        
        return result
    except Exception as e:
        return f"Error reading health events: {str(e)}"

@mcp.tool()
def search_health_events(
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
        query: Text to search for in narratives
        event_type: Optional filter by event type
        start_date: Optional filter after this date (YYYY-MM-DD)
        end_date: Optional filter before this date (YYYY-MM-DD)
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
            # Check text match in narrative
            if query_lower not in event['narrative'].lower():
                # Also check structured data
                if query_lower not in json.dumps(event.get('structured', {})).lower():
                    continue
            
            # Check event type if specified
            if event_type and event['type'].lower() != event_type.lower():
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
    
    This is a simplified version - in practice, Claude would use
    its understanding to extract more accurate information.
    """
    extracted = {
        "symptoms": [],
        "diagnoses": [],
        "medications": [],
        "test_results": [],
        "recommendations": [],
        "providers": []
    }
    
    # Simple keyword extraction
    narrative_lower = narrative.lower()
    
    # Look for symptoms
    symptom_keywords = ["pain", "ache", "fever", "cough", "fatigue", "nausea", "gas", "bloating"]
    for keyword in symptom_keywords:
        if keyword in narrative_lower:
            extracted["symptoms"].append(keyword)
    
    # Look for diagnoses
    if "cholesterol" in narrative_lower and ("high" in narrative_lower or "elevated" in narrative_lower):
        extracted["diagnoses"].append("high cholesterol")
    if "diabetes" in narrative_lower:
        extracted["diagnoses"].append("diabetes")
    if "hypertension" in narrative_lower or "blood pressure" in narrative_lower:
        extracted["diagnoses"].append("hypertension")
    
    # Look for medications
    medication_keywords = {
        "statin": "statin medication",
        "atorvastatin": "atorvastatin (statin)",
        "metformin": "metformin",
        "aspirin": "aspirin",
        "ibuprofen": "ibuprofen"
    }
    for keyword, med_name in medication_keywords.items():
        if keyword in narrative_lower:
            extracted["medications"].append({
                "name": med_name,
                "status": "mentioned"
            })
    
    # Look for recommendations
    if ("walk" in narrative_lower or "exercise" in narrative_lower) and "more" in narrative_lower:
        extracted["recommendations"].append("increase physical activity")
    if "diet" in narrative_lower:
        extracted["recommendations"].append("dietary changes")
    
    # Look for providers
    if "doctor" in narrative_lower or "dr." in narrative_lower:
        extracted["providers"].append("doctor")
    if "specialist" in narrative_lower:
        extracted["providers"].append("specialist")
    
    return json.dumps(extracted, indent=2)

@mcp.tool()
def save_conversation(
    user_id: str,
    conversation: str,
    date: Optional[str] = None
) -> str:
    """
    Save a conversation for future reference.
    
    Args:
        user_id: User identifier
        conversation: The conversation text
        date: Optional date, defaults to today
    """
    try:
        date_str = date or datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H-%M-%S")
        
        conv_file = WORKSPACE_DIR / "conversations" / f"{user_id}_{date_str}_{timestamp}.md"
        
        with open(conv_file, "w") as f:
            f.write(f"# Health Conversation - {date_str} {timestamp}\n\n")
            f.write(f"User: {user_id}\n\n")
            f.write("---\n\n")
            f.write(conversation)
        
        return f"Saved conversation to {conv_file.name}"
    except Exception as e:
        return f"Error saving conversation: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")