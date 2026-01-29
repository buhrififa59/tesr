import os
import database_supabase as db
from dotenv import load_dotenv

load_dotenv()

print(f"Supabase URL: {os.environ.get('SUPABASE_URL')}")
print("Initializing Supabase...")

if db.init_supabase():
    print("✅ Supabase initialized.")
    try:
        client = db.get_supabase_client()
        print("Testing query to 'teachers' table...")
        
        # Try to select just one record to see if it works
        response = client.table('teachers').select('id, name', count='exact').limit(1).execute()
        
        print(f"✅ Connection successful!")
        print(f"📊 Total records: {response.count}")
        if response.data:
            print(f"📝 First teacher: {response.data[0]}")
        else:
            print("📝 No teachers found (but connection worked)")
            
    except Exception as e:
        print(f"❌ Query failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ Failed to initialize Supabase client.")
