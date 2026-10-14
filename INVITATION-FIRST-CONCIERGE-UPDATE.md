# Concierge invitation-first update

The master personality prompt now prioritizes a personalized invitation as the first response following identification and any configured verification. The profile determines emotional tone and relationship-specific reasons to attend. After the initial invitation, the assistant moves to proactive, varied conversation and answers factual questions directly. Avoid repeated pressure.

Changed: backend/concierge_personality.py and backend/concierge.py.

Testing: compile the Python files and run your usual end-to-end guest identification, verification and first-message flow.
