# Slalom Capabilities Management API

<p align="center">
  <img src="https://colby-timm.github.io/images/byte-teacher.png" alt="Byte Teacher" width="200" />
</p>

A FastAPI application that enables Slalom consultants to register their capabilities and manage consulting expertise across the organization.

## Features

- View all available consulting capabilities
- Create and update consultant profiles independently of capability registration
- Register consultant expertise and availability
- Persist consultant profiles and capability assignments in a local JSON store
- Manage capability capacity and team assignments

## Getting Started

1. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the application:

   ```
   python -m uvicorn src.app:app --reload
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc
   - Capabilities Dashboard: http://localhost:8000/

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/capabilities`                                                   | Get all capabilities with details and current consultant assignments |
| GET    | `/consultants`                                                   | List consultant profiles and their assigned capabilities             |
| GET    | `/consultants/{email}`                                           | Get an individual consultant profile                                |
| POST   | `/consultants`                                                   | Create a consultant profile                                          |
| PATCH  | `/consultants/{email}`                                           | Update a consultant profile                                          |
| POST   | `/capabilities/{capability_name}/register?email=consultant@slalom.com` | Register consultant for a capability                     |
| DELETE | `/capabilities/{capability_name}/unregister?email=consultant@slalom.com` | Unregister consultant from a capability              |

## Data Model

The application uses a consulting-focused data model:

1. **Capabilities** - Uses capability name as identifier:
   - Description of the consulting capability
   - Skill levels (Emerging, Proficient, Advanced, Expert)
   - Practice area (Strategy, Technology, Operations)
   - Industry verticals served
   - Required certifications
   - List of consultant profile references registered to the capability
   - Available capacity (hours per week)

2. **Consultants** - Uses email as identifier:
   - Name
   - Practice area
   - Skills
   - Certifications
   - Availability
   - Current capability assignments

Application data is persisted in `src/data/store.json`. The app seeds that file automatically the first time it starts so consultant profiles, capabilities, and assignments survive restart.

## Future Enhancements

This exercise will guide you through implementing:
- Capability maturity assessments
- Intelligent team matching algorithms  
- Analytics dashboards for practice leads
- Integration with project management systems
- Advanced search and filtering capabilities
