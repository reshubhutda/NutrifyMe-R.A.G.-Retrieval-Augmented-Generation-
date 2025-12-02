from build_nutrition_db import build_nutrition_collection
from build_health_db import build_health_collection
from build_reference_db import build_reference_collection

# Main console to store data in ChromaDB

if __name__ == "__main__":
    print("\n=== Building ALL vector databases ===\n")

    build_nutrition_collection()
    build_health_collection()
    build_reference_collection()

    print("\n=== ALL vector DBs built successfully ===\n")