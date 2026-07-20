#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
fixtures=ROOT/"tests"/"fixtures"

count=sum(1 for _ in fixtures.rglob("*.monkey"))
print(f"Fixture scan complete: {count} source file(s)")
