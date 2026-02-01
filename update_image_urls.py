import os
from supabase import create_client

# Configuration
OLD_BASE_URL = "https://hbbqwcesmwqnfgkmdayp.supabase.co"
NEW_BASE_URL = "https://uqbfndzztozlkorciykf.supabase.co"

# Use Service Role Key to ensure we can update rows
# (User provided this in previous step)
SUPABASE_URL = NEW_BASE_URL
SUPABASE_SERVICE_KEY = "PLACEHOLDER_SERVICE_ROLE_KEY" # ⚠️ REMOVED FOR SECURITY

def update_urls():
    print("🔄 Starting Profile Picture URL Update...")
    
    conn = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # 1. Fetch current data
    print("   Fetching teachers...")
    response = conn.table("teachers").select("id, username, profile_picture").execute()
    teachers = response.data
    
    updated_count = 0
    
    # 2. Iterate and Update
    for teacher in teachers:
        old_url = teacher.get('profile_picture')
        
        if not old_url:
            continue
            
        if OLD_BASE_URL in old_url:
            new_url = old_url.replace(OLD_BASE_URL, NEW_BASE_URL)
            
            print(f"   📝 Updating {teacher['username']}...")
            print(f"      Old: {old_url[:50]}...")
            print(f"      New: {new_url[:50]}...")
            
            try:
                conn.table("teachers").update({"profile_picture": new_url}).eq("id", teacher['id']).execute()
                updated_count += 1
            except Exception as e:
                print(f"      ❌ Failed: {e}")
    
    if updated_count == 0:
        print("\nℹ️ No URLs needed updating (maybe already done?).")
    else:
        print(f"\n✅ Successfully updated {updated_count} records!")

if __name__ == "__main__":
    update_urls()
