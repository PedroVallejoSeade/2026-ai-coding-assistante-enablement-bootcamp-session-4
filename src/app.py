"""Slalom Capabilities Management System API."""

import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(
    title="Slalom Capabilities Management API",
    description="API for managing consulting capabilities and consultant expertise",
)

current_dir = Path(__file__).parent
data_dir = current_dir / "data"
data_file = data_dir / "store.json"
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(current_dir, "static")),
    name="static",
)

DEFAULT_CAPABILITIES = {
    "Cloud Architecture": {
        "description": "Design and implement scalable cloud solutions using AWS, Azure, and GCP",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["AWS Solutions Architect", "Azure Architect Expert"],
        "industry_verticals": ["Healthcare", "Financial Services", "Retail"],
        "capacity": 40,
        "consultants": ["alice.smith@slalom.com", "bob.johnson@slalom.com"],
    },
    "Data Analytics": {
        "description": "Advanced data analysis, visualization, and machine learning solutions",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Tableau Desktop Specialist", "Power BI Expert", "Google Analytics"],
        "industry_verticals": ["Retail", "Healthcare", "Manufacturing"],
        "capacity": 35,
        "consultants": ["emma.davis@slalom.com", "sophia.wilson@slalom.com"],
    },
    "DevOps Engineering": {
        "description": "CI/CD pipeline design, infrastructure automation, and containerization",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Docker Certified Associate", "Kubernetes Admin", "Jenkins Certified"],
        "industry_verticals": ["Technology", "Financial Services"],
        "capacity": 30,
        "consultants": ["john.brown@slalom.com", "olivia.taylor@slalom.com"],
    },
    "Digital Strategy": {
        "description": "Digital transformation planning and strategic technology roadmaps",
        "practice_area": "Strategy",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Digital Transformation Certificate", "Agile Certified Practitioner"],
        "industry_verticals": ["Healthcare", "Financial Services", "Government"],
        "capacity": 25,
        "consultants": ["liam.anderson@slalom.com", "noah.martinez@slalom.com"],
    },
    "Change Management": {
        "description": "Organizational change leadership and adoption strategies",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Prosci Certified", "Lean Six Sigma Black Belt"],
        "industry_verticals": ["Healthcare", "Manufacturing", "Government"],
        "capacity": 20,
        "consultants": ["ava.garcia@slalom.com", "mia.rodriguez@slalom.com"],
    },
    "UX/UI Design": {
        "description": "User experience design and digital product innovation",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Adobe Certified Expert", "Google UX Design Certificate"],
        "industry_verticals": ["Retail", "Healthcare", "Technology"],
        "capacity": 30,
        "consultants": ["amelia.lee@slalom.com", "harper.white@slalom.com"],
    },
    "Cybersecurity": {
        "description": "Information security strategy, risk assessment, and compliance",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["CISSP", "CISM", "CompTIA Security+"],
        "industry_verticals": ["Financial Services", "Healthcare", "Government"],
        "capacity": 25,
        "consultants": ["ella.clark@slalom.com", "scarlett.lewis@slalom.com"],
    },
    "Business Intelligence": {
        "description": "Enterprise reporting, data warehousing, and business analytics",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Microsoft BI Certification", "Qlik Sense Certified"],
        "industry_verticals": ["Retail", "Manufacturing", "Financial Services"],
        "capacity": 35,
        "consultants": ["james.walker@slalom.com", "benjamin.hall@slalom.com"],
    },
    "Agile Coaching": {
        "description": "Agile transformation and team coaching for scaled delivery",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Certified Scrum Master", "SAFe Agilist", "ICAgile Certified"],
        "industry_verticals": ["Technology", "Financial Services", "Healthcare"],
        "capacity": 20,
        "consultants": ["charlotte.young@slalom.com", "henry.king@slalom.com"],
    },
}


class ConsultantCreate(BaseModel):
    email: str
    name: str | None = None
    practice_area: str | None = None
    availability: str | None = None
    certifications: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)


class ConsultantUpdate(BaseModel):
    name: str | None = None
    practice_area: str | None = None
    availability: str | None = None
    certifications: list[str] | None = None
    skills: list[str] | None = None


def normalize_email(email: str) -> str:
    return email.strip().lower()


def build_display_name(email: str) -> str:
    local_part = email.split("@", maxsplit=1)[0]
    return " ".join(part.capitalize() for part in local_part.split("."))


def build_consultant_profile(email: str, practice_area: str | None = None) -> dict:
    return {
        "email": email,
        "name": build_display_name(email),
        "practice_area": practice_area or "Unassigned",
        "availability": "Unknown",
        "certifications": [],
        "skills": [],
    }


def build_default_store() -> dict:
    consultants = {}
    capabilities = {}

    for capability_name, details in DEFAULT_CAPABILITIES.items():
        consultant_emails = [normalize_email(email) for email in details["consultants"]]
        capabilities[capability_name] = {
            key: value for key, value in details.items() if key != "consultants"
        }
        capabilities[capability_name]["consultants"] = consultant_emails

        for email in consultant_emails:
            consultants.setdefault(
                email,
                build_consultant_profile(email, details.get("practice_area")),
            )

    return {"consultants": consultants, "capabilities": capabilities}


def save_store(store: dict) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    data_file.write_text(json.dumps(store, indent=2), encoding="utf-8")


def load_store() -> dict:
    if not data_file.exists():
        default_store = build_default_store()
        save_store(default_store)
        return default_store

    loaded_store = json.loads(data_file.read_text(encoding="utf-8"))
    loaded_store.setdefault("consultants", {})
    loaded_store.setdefault("capabilities", {})
    return loaded_store


store = load_store()


def get_consultant_capabilities() -> dict[str, list[str]]:
    consultant_capabilities = {email: [] for email in store["consultants"]}

    for capability_name, details in store["capabilities"].items():
        for email in details.get("consultants", []):
            consultant_capabilities.setdefault(email, []).append(capability_name)

    return consultant_capabilities


def serialize_consultant(email: str) -> dict:
    consultant = dict(store["consultants"][email])
    consultant["capabilities"] = get_consultant_capabilities().get(email, [])
    return consultant


def serialize_capabilities() -> dict:
    serialized = {}

    for capability_name, details in store["capabilities"].items():
        consultant_profiles = []
        for email in details.get("consultants", []):
            profile = store["consultants"].get(email)
            if profile is not None:
                consultant_profiles.append(dict(profile))

        serialized[capability_name] = {
            **details,
            "consultants": consultant_profiles,
        }

    return serialized


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/capabilities")
def get_capabilities():
    return serialize_capabilities()


@app.get("/consultants")
def get_consultants():
    return [
        serialize_consultant(email)
        for email in sorted(store["consultants"])
    ]


@app.get("/consultants/{email}")
def get_consultant(email: str):
    normalized_email = normalize_email(email)
    if normalized_email not in store["consultants"]:
        raise HTTPException(status_code=404, detail="Consultant not found")

    return serialize_consultant(normalized_email)


@app.post("/consultants")
def create_consultant(consultant: ConsultantCreate):
    normalized_email = normalize_email(consultant.email)
    if normalized_email in store["consultants"]:
        raise HTTPException(status_code=400, detail="Consultant already exists")

    consultant_profile = build_consultant_profile(
        normalized_email,
        consultant.practice_area,
    )
    consultant_profile.update(
        consultant.model_dump(exclude={"email"}, exclude_none=True)
    )
    consultant_profile["email"] = normalized_email
    store["consultants"][normalized_email] = consultant_profile
    save_store(store)
    return serialize_consultant(normalized_email)


@app.patch("/consultants/{email}")
def update_consultant(email: str, consultant: ConsultantUpdate):
    normalized_email = normalize_email(email)
    if normalized_email not in store["consultants"]:
        raise HTTPException(status_code=404, detail="Consultant not found")

    consultant_updates = consultant.model_dump(exclude_none=True)
    store["consultants"][normalized_email].update(consultant_updates)
    save_store(store)
    return serialize_consultant(normalized_email)


@app.post("/capabilities/{capability_name}/register")
def register_for_capability(capability_name: str, email: str):
    """Register a consultant for a capability."""
    if capability_name not in store["capabilities"]:
        raise HTTPException(status_code=404, detail="Capability not found")

    normalized_email = normalize_email(email)
    capability = store["capabilities"][capability_name]

    if normalized_email in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is already registered for this capability",
        )

    if normalized_email not in store["consultants"]:
        store["consultants"][normalized_email] = build_consultant_profile(
            normalized_email,
            capability.get("practice_area"),
        )

    capability["consultants"].append(normalized_email)
    save_store(store)
    return {"message": f"Registered {normalized_email} for {capability_name}"}


@app.delete("/capabilities/{capability_name}/unregister")
def unregister_from_capability(capability_name: str, email: str):
    """Unregister a consultant from a capability."""
    if capability_name not in store["capabilities"]:
        raise HTTPException(status_code=404, detail="Capability not found")

    normalized_email = normalize_email(email)
    capability = store["capabilities"][capability_name]

    if normalized_email not in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is not registered for this capability",
        )

    capability["consultants"].remove(normalized_email)
    save_store(store)
    return {"message": f"Unregistered {normalized_email} from {capability_name}"}
