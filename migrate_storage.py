import os
import requests
from supabase import create_client, Client

# OLD Database (Source)
OLD_URL = "https://hbbqwcesmwqnfgkmdayp.supabase.co"
OLD_KEY = "sb_publishable_Ln1_Vu-1Moho5_l6CsfMIQ_ZwVpPcj6" 

# NEW Database (Destination)
NEW_URL = "https://uqbfndzztozlkorciykf.supabase.co"
NEW_KEY = "PLACEHOLDER_SERVICE_ROLE_KEY" # ⚠️ REMOVED FOR SECURITY. Use your Service Role Key here found in Supabase Settings > API

# Buckets to migrate
BUCKETS = ["profile-pictures"] # Corrected bucket name

def get_client(url, key) -> Client:
    return create_client(url, key)

def migrate_storage():
    print("📦 Starting Storage Migration...")
    
    old_client = get_client(OLD_URL, OLD_KEY)
    new_client = get_client(NEW_URL, NEW_KEY)
    
    # Ensure temp directory exists
    os.makedirs("temp_downloads", exist_ok=True)
    
    for bucket in BUCKETS:
        print(f"\n📂 Processing bucket: {bucket}")
        
        # 1. List files in OLD bucket
        try:
            files = old_client.storage.from_(bucket).list()
        except Exception as e:
            print(f"   ⚠️ Could not list bucket '{bucket}' in OLD DB (maybe it doesn't exist?): {e}")
            continue
            
        if not files:
            print("   ℹ️ Bucket is empty.")
            continue
            
        print(f"   found {len(files)} files.")
        
        # 2. Upload to NEW bucket
        for file in files:
            file_name = file['name']
            print(f"   ⬇️ Downloading {file_name}...")
            
            try:
                # Download
                data = old_client.storage.from_(bucket).download(file_name)
                temp_path = f"temp_downloads/{file_name}"
                with open(temp_path, "wb") as f:
                    f.write(data)
                
                # Upload
                print(f"   ⬆️ Uploading to NEW DB...")
                # Check if bucket exists in NEW, if not create it (requires admin/service role usually, but try)
                # Note: creating bucket via API isn't always open to Anon. Assuming buckets exist manually.
                
                with open(temp_path, "rb") as f:
                    new_client.storage.from_(bucket).upload(file_name, f, {"content-type": file.get("metadata", {}).get("mimetype", "application/octet-stream")})
                
                print(f"   ✅ Migrated {file_name}")
                
                # Cleanup
                os.remove(temp_path)
                
            except Exception as e:
                print(f"   ❌ Failed to migrate {file_name}: {e}")

    # Cleanup directory
    try:
        os.rmdir("temp_downloads")
    except:
        pass
        
    print("\n✨ Storage Migration Complete!")

if __name__ == "__main__":
    migrate_storage()
