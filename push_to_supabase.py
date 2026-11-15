"""
Utility script to verify Supabase Cloud Database connection
and synchronize all tables and franchise squads.
"""

import sys
from supabase_sync import sync_push_all_to_supabase, is_supabase_enabled
from database import get_supabase_client


def main():
    print("=" * 60)
    print("🏏 IPL AUCTION SYSTEM - SUPABASE SYNC VERIFICATION")
    print("=" * 60)

    if not is_supabase_enabled():
        print("❌ Supabase is not enabled in .env (DB_MODE must be 'supabase')")
        return

    sb = get_supabase_client()
    if not sb:
        print("❌ Could not connect to Supabase client. Check .env SUPABASE_URL and SUPABASE_KEY.")
        return

    print("✅ Connected to Supabase project!")
    print("📡 Testing table access and Row Level Security (RLS)...")

    try:
        res = sb.table("teams").select("count", count="exact").execute()
        print(f"  • Teams table: {res.count} records")
    except Exception as e:
        print(f"  ⚠️ Teams table check: {e}")

    try:
        res = sb.table("players").select("count", count="exact").execute()
        print(f"  • Players table: {res.count} records")
    except Exception as e:
        print(f"  ⚠️ Players table check: {e}")

    print("\n🔄 Pushing all current SQLite records to Supabase...")
    sync_res = sync_push_all_to_supabase()
    if sync_res.get("success"):
        print("✅ FULL SYNC COMPLETED SUCCESSFULLY!")
        print("📊 Synced items:", sync_res.get("results"))
    else:
        print("⚠️ Sync notice:", sync_res.get("error") or sync_res.get("message"))
        print("\n💡 Tip: Please ensure you ran 'supabase_schema.sql' in your Supabase SQL Editor")
        print("   so that all 14 tables and RLS permissions are created!")


if __name__ == "__main__":
    main()
