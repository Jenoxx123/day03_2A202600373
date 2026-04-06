# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: [Huynh Thai Bao]
- **Student ID**: [2A202600373]
- **Date**: [06/04/2026]

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implementated**: [src/chatbot_baseline.py]
- **Code Highlights**: [Copy snippets or link file lines]
- **Documentation**: [My code establishes a standardized testing environment. The baseline chatbot provides a direct response using the LLM, while the mock data serves as the input "ground truth" to observe how the ReAct loop utilizes available tools to verify information versus the baseline's tendency to hallucinate.]

---

## II. Debugging Case Study (10 Points)


*Implemented a robust Backend for a Calendar Booking Agent using Google Calendar API with OAuth 2.0 authentication, supporting multi-user availability checks and automated invitations.*

- **Modules Implementated**: `src/backend/main.py`, `credentials.json`, `token.json` (auto-generated).
- **Code Highlights**:
  - **Auto-Auth OAuth 2.0 Logic**: Developed a `get_calendar_service()` function that detects missing or expired tokens and automatically triggers a local server for browser-based login. This ensures portability across different team members' machines.
  - **Flexible Multi-Attendee Support**: Refactored the `BookingRequest` schema to accept a `List[str]` for `target_email`, moving away from hardcoded environment variables to a dynamic input system.
  - **Comprehensive FreeBusy API**: Integrated the Google `freebusy.query` method to check the "primary" user and all requested attendees simultaneously before committing any write actions.
- **Documentation**: The backend exposes two primary endpoints for the ReAct loop:
  1. `POST /calendar/check`: Returns a boolean `available` and a list of `busy_users` for the Agent's "Observation" phase.
  2. `POST /calendar/book`: Executes the "Action" phase by creating events and sending email invitations with `sendUpdates='all'`.
---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Resolved a critical authentication failure and permission mismatch during the transition from Service Accounts to OAuth 2.0.*

- 1.  **Reasoning**: The `Thought` block is crucial for the Calendar tool. While a standard Chatbot might prematurely confirm a meeting, the ReAct Agent uses the `Thought` process to realize it *must* validate availability via the `/check` tool before attempting to execute the `/book` tool.
2.  **Reliability**: The Agent can perform worse than a Chatbot if the user provides ambiguous time inputs (e.g., "next Monday afternoon"). Without a high-precision NLP date-parser, the Agent might generate invalid ISO strings, leading to API failures.
3.  **Observation**: Environment feedback (Observations) directly dictates the Agent's branching logic. For example, receiving a `busy_users` list allows the Agent to pivot from "Booking" to "Proposing an alternative time," showcasing higher cognitive adaptability than a static script.
---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Implement an **Asynchronous Task Queue** (e.g., Celery with FastAPI) to handle high-frequency booking requests and manage Google API rate limits effectively.
- **Safety**: Introduce a **Human-in-the-loop** confirmation step where the Agent displays a summary of the meeting details and waits for a final "Confirm" button click before calling the `/book` endpoint.
- **Performance**: Integrate a dedicated **NLP Temporal Parser** (like Facebook's `Duckling`) to translate messy natural language into precise ISO-8601 timestamps, reducing the error rate for the Backend API.

---

> [!NOTE]
> Submit this report by renaming it to `REPORT_[YOUR_NAME].md` and placing it in this folder.
