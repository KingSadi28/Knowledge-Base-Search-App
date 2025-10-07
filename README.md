# wand-ai-assignment

## Design Decisions

- Adopted FastAPI for rapid API development and automatic documentation.
- Maintained a modular structure for clarity and scalability.
- Leveraged standard Python libraries alongside FastAPI to minimize dependencies.

## Trade-offs Due to 24h Constraint

- Limited error handling, and input validation.
- Skipped advanced optimizations, completeness check and comprehensive testing.
- Focused on core API features over frontend or UI enhancements.

## How to Run/Test

1. Ensure Python 3.11 or higher is installed.
2. Create and activate venv
    python -m venv venv
    source venv/bin/activate
2. Install from requirements.txt
    pip install -r requirements.txt
3. From the `app` folder, run:
    ```bash
    uvicorn main:app --reload
    ```