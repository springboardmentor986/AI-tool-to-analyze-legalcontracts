# pinecone_test.py  (place in ClauseAI/ root)
# Run: python pinecone_test.py
# Purpose: verifies Pinecone connection + index access + stats + upsert/query works.

import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "").strip()

# Use ONE of these in .env (supporting both names):
# PINECONE_INDEX=clauseai-gemini
# OR
# PINECONE_INDEX_NAME=clauseai-gemini
PINECONE_INDEX = (os.getenv("PINECONE_INDEX") or os.getenv("PINECONE_INDEX_NAME") or "clauseai-gemini").strip()

# Optional: if you want to connect via host directly
PINECONE_HOST = os.getenv("PINECONE_HOST", "").strip()

# If DIM is not set, we will auto-read it from Pinecone index info.
DIM_ENV = os.getenv("PINECONE_DIM", "").strip()

if not PINECONE_API_KEY:
    print("❌ Missing PINECONE_API_KEY in .env")
    sys.exit(1)

try:
    from pinecone import Pinecone
except Exception as e:
    print("❌ Pinecone import failed. Try:")
    print('   pip install -U "pinecone[asyncio]>=6,<8" python-dotenv')
    print("Error:", e)
    sys.exit(1)


def main():
    print("🔧 Pinecone test starting...")
    print("Index name:", PINECONE_INDEX)
    print("Host set:", bool(PINECONE_HOST))

    pc = Pinecone(api_key=PINECONE_API_KEY)

    # 1) List indexes (proves account access)
    try:
        indexes = pc.list_indexes()
        print("✅ list_indexes OK")
        print("Indexes:", indexes)
    except Exception as e:
        print("❌ list_indexes failed:", e)
        sys.exit(1)

    # 2) Connect to index
    try:
        if PINECONE_HOST:
            index = pc.Index(host=PINECONE_HOST)
            print("✅ Connected via host")
        else:
            index = pc.Index(PINECONE_INDEX)
            print("✅ Connected via index name")
    except Exception as e:
        print("❌ Index connect failed:", e)
        print("Tip: If you see host/permission errors, set PINECONE_HOST from Pinecone console.")
        sys.exit(1)

    # 3) Show index info + stats (THIS is the “show Pinecone DB” part)
    try:
        info = pc.describe_index(PINECONE_INDEX)
        index_dim = getattr(info, "dimension", None) or info.get("dimension", None)  # supports dict/object
        metric = getattr(info, "metric", None) or info.get("metric", None)
        print("\n📌 Index info:")
        print(" - dimension:", index_dim)
        print(" - metric:", metric)
    except Exception as e:
        # Not fatal; some SDK versions differ. We'll still show stats.
        print("⚠️ Could not fetch describe_index info:", e)
        index_dim = None

    try:
        stats = index.describe_index_stats()
        print("\n📊 describe_index_stats():")
        print(stats)
    except Exception as e:
        print("❌ describe_index_stats failed:", e)
        sys.exit(1)

    # 4) Decide dimension for test vector
    if DIM_ENV:
        dim = int(DIM_ENV)
        print("\nExpected dimension (from env PINECONE_DIM):", dim)
        if index_dim and dim != int(index_dim):
            print(f"❌ Dimension mismatch: env DIM={dim} but index DIM={index_dim}")
if __name__ == "__main__":
    main()
    