import uvicorn
import os
import sys

# Configure UTF-8 for Windows console compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    sys.path.insert(0, current_dir)
    print(">> Starting AnnaSetu Modular Backend on http://127.0.0.1:8000 ...")
    print(">> Interactive Swagger Docs: http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
