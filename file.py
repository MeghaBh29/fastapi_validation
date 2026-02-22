from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import BytesIO

app = FastAPI()

# ✅ Enable CORS for any origin and POST requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow requests from anywhere
    allow_methods=["*"],   # Only POST requests
    allow_headers=["*"],      # Allow all headers, including custom ones
)

# File upload endpoint
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_5104: str = Header(None)
):
    # 1️⃣ Check authentication
    if x_upload_token_5104 != "k2v6nq8fu0avc3w2":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2️⃣ Check file type
    allowed_types = [".csv", ".json", ".txt"]
    if not any(file.filename.endswith(ext) for ext in allowed_types):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 3️⃣ Check file size (max 65KB)
    contents = await file.read()
    max_size = 65 * 1024  # 65 KB
    if len(contents) > max_size:
        raise HTTPException(status_code=413, detail="File too large")

    # 4️⃣ If CSV, parse and compute stats
    if file.filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(contents))

        total_value = float(df['value'].sum()) if 'value' in df.columns else 0
        category_counts = df['category'].value_counts().to_dict() if 'category' in df.columns else {}

        return {
            "email": "21f1000341@ds.study.iitm.ac.in",
            "filename": file.filename,
            "rows": len(df),
            "columns": df.columns.tolist(),
            "totalValue": total_value,
            "categoryCounts": category_counts
        }

    # For other allowed types, just acknowledge upload
    return {"filename": file.filename, "status": "Uploaded successfully"}