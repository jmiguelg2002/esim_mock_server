from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mock SES & eSIM Server")

# In-memory IMSI to user/profile store
user_profiles = {
    "714011002222222": {
        "user_id": "user_001",
        "esim_provisioned": True,
        "profile_id": "eSim-2222",
        "operator": "TelcoX"
    },
    "714011002333333": {
        "user_id": "user_002",
        "esim_provisioned": True,
        "profile_id": "eSim-3333",
        "operator": "TelcoX"
    },
    "714011002444444": {
        "user_id": "user_003",
        "esim_provisioned": True,
        "profile_id": "eSim-4444",
        "operator": "TelcoX"
    },
    "714011002555555": {
        "user_id": "user_004",
        "esim_provisioned": True,
        "profile_id": "eSim-5555",
        "operator": "TelcoX"
    },
    # Example unprovisioned IMSI for testing
    "714011003333333": {
        "user_id": "user_005",
        "esim_provisioned": False
    }
}

class ValidateRequest(BaseModel):
    imsi: str

class ProvisionRequest(BaseModel):
    imsi: str
    operator: Optional[str] = "DefaultTelco"

@app.post("/validate")
def validate_imsi(req: ValidateRequest):
    profile = user_profiles.get(req.imsi)
    if profile:
        return {
            "user_id": profile.get("user_id"),
            "esim_provisioned": profile.get("esim_provisioned", False),
            "profile_id": profile.get("profile_id", None),
            "operator": profile.get("operator", None)
        }
    raise HTTPException(status_code=404, detail="IMSI not found")

@app.post("/provision")
def provision_esim(req: ProvisionRequest):
    profile = user_profiles.get(req.imsi)
    if profile:
        if profile.get("esim_provisioned"):
            return {
                "message": "Already provisioned",
                "user_id": profile["user_id"],
                "profile_id": profile["profile_id"],
                "operator": profile.get("operator", "Unknown")
            }
        # Simulate provisioning
        profile["esim_provisioned"] = True
        profile["profile_id"] = f"eSim-{req.imsi[-4:]}"
        profile["operator"] = req.operator
        return {
            "message": "Provisioned successfully",
            "user_id": profile["user_id"],
            "profile_id": profile["profile_id"],
            "operator": req.operator
        }
    raise HTTPException(status_code=404, detail="IMSI not found for provisioning")
