from app.core.database import SessionLocal
from app.services.global_location_service import global_location_service

db = SessionLocal()

print("--- 1. Autocomplete China ---")
for item in global_location_service.autocomplete(db, "China"):
    print(f"  * {item['title']} ({item['type']}) | canonical_id: {item['canonical_id']} | country: {item['country']}")

print("\n--- 2. Autocomplete Beijing (prefix 'Beij') ---")
for item in global_location_service.autocomplete(db, "Beij"):
    print(f"  * {item['title']} ({item['type']}) | canonical_id: {item['canonical_id']} | coords: ({item['latitude']}, {item['longitude']})")

print("\n--- 3. Autocomplete Paris (prefix 'Par') ---")
for item in global_location_service.autocomplete(db, "Par"):
    print(f"  * {item['title']} ({item['type']}) | canonical_id: {item['canonical_id']}")

print("\n--- 4. Autocomplete Tokyo (prefix 'Tok') ---")
for item in global_location_service.autocomplete(db, "Tok"):
    print(f"  * {item['title']} ({item['type']}) | canonical_id: {item['canonical_id']}")

print("\n--- 5. Autocomplete Jaipur (prefix 'Jaip') ---")
for item in global_location_service.autocomplete(db, "Jaip"):
    print(f"  * {item['title']} ({item['type']}) | canonical_id: {item['canonical_id']}")

print("\n--- 6. Testing Resolution of China, Beijing, Jaipur, London, Sydney, Cairo ---")
for place in ["China", "Beijing", "Jaipur", "London", "Sydney", "Cairo", "country:china:cn", "city:beijing:cn"]:
    res = global_location_service.resolve(db, place)
    assert res is not None, f"Failed to resolve {place}"
    print(f"  * Resolved '{place}': Name={res.get('name')}, Country={res.get('country_name')}, Lat={res.get('latitude')}, POIs={len(res.get('attractions', []))}")

print("\nBackend Service Verification: SUCCESS!")
