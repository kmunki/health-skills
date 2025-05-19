# Health Assist Implementation Plan

## Project Overview

Health Assist is a personal health narrative tracking system that helps users capture their health story through natural conversation. Unlike official health records, this captures the user's own narrative - the way they experience and remember their health journey.

## Architecture: Hybrid Approach

Combining MCP tools with Claude's natural conversation abilities:
- Use tools for data operations (save, retrieve, update)
- Let Claude handle the natural conversation flow
- Claude automatically invokes tools based on conversation content

## Implementation Strategy

### Phase 1: Core Data Structure
```
workspace/
├── narratives/
│   └── {user}_narrative.md     # Human-readable story
├── structured/
│   └── {user}_events.json      # Structured health events
└── conversations/
    └── {user}_chat_{date}.md   # Conversation logs
```

### Phase 2: Smart Tools Design

1. **`save_health_event`**
   - Parameters: narrative_text, structured_data, user_id
   - Saves both narrative and JSON versions

2. **`get_health_narrative`**
   - Returns the current narrative for display/editing

3. **`search_health_events`**
   - Query structured data by date, type, medication, etc.

4. **`update_narrative_style`**
   - Adjusts tone/style based on user preferences

### Phase 3: Conversation Flow

Claude would:
1. Listen to user's natural speech
2. Extract key health information
3. Automatically invoke tools to save data
4. Respond with verification/clarification

## Key Design Decisions

### 1. Implicit Tool Usage
- User never needs to know about tools
- Claude decides when to save/update based on content
- Tools are invoked transparently

### 2. Dual Storage Format
- **Narrative**: Markdown files preserving user's voice
- **Structured**: JSON for queries and analysis
- Both updated simultaneously

### 3. Conversation Intelligence
- Claude maintains context across sessions
- Asks clarifying questions naturally
- Builds comprehensive health story over time

### 4. Privacy-First Design
- All data stays local in workspace
- No external APIs or cloud storage
- User owns their complete health narrative

## Example Flow

```
User: "Doc said my cholesterol is high, starting a statin"
↓
Claude processes:
- Extracts: doctor visit, cholesterol diagnosis, medication
- Invokes: save_health_event(narrative, json_data)
- Responds: "I've noted your visit today about cholesterol..."
```

## JSON Schema (To Be Defined)

Example health event structure:
```json
{
  "id": "uuid",
  "user_id": "bob",
  "date": "2025-01-19",
  "type": "doctor_visit",
  "narrative": "Doc said my cholesterol is high...",
  "structured": {
    "diagnosis": ["high cholesterol"],
    "medications": [{
      "name": "atorvastatin",
      "status": "started"
    }],
    "recommendations": ["walk more"]
  }
}
```

## Development Phases

1. **Phase 1**: Define JSON schema for health events
2. **Phase 2**: Create basic CRUD tools
3. **Phase 3**: Implement narrative generation
4. **Phase 4**: Build conversation intelligence
5. **Phase 5**: Add search and query capabilities

## Success Criteria

- Users can have natural health conversations
- Data is captured in both narrative and structured formats
- Historical health information is searchable
- User's voice and style are preserved
- All data remains private and local