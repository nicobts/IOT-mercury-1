#!/usr/bin/env python3
"""
Test script for 1NCE API connection
Run this to verify your API credentials are working
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.client import OnceAPIClient
from src.utils.logger import setup_logging

def test_api():
    """Test 1NCE API connection and endpoints"""
    setup_logging()
    print("=" * 60)
    print("1NCE API Connection Test")
    print("=" * 60)

    try:
        client = OnceAPIClient()

        # Test 1: Authentication
        print("\n[1/4] Testing authentication...")
        token = client.auth_manager.get_token()
        print(f"✓ Authentication successful! Token: {token[:20]}...")

        # Test 2: Get all SIMs
        print("\n[2/4] Testing get all SIMs...")
        sims = client.get_all_sims()
        print(f"✓ Found {len(sims)} SIM cards")

        if sims:
            # Test 3: Get single SIM details
            print("\n[3/4] Testing get single SIM...")
            iccid = sims[0]['iccid']
            sim_detail = client.get_sim(iccid)
            print(f"✓ SIM details retrieved for {iccid}")
            print(f"  - Label: {sim_detail.get('label', 'No label')}")
            print(f"  - Status: {sim_detail.get('status', 'Unknown')}")
            print(f"  - IMSI: {sim_detail.get('imsi', 'N/A')}")

            # Test 4: Get usage data
            print("\n[4/4] Testing get usage data...")
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

            try:
                usage = client.get_sim_usage(iccid, start_date, end_date)
                stats = usage.get('stats', [])
                print(f"✓ Usage data retrieved: {len(stats)} days of data")

                if stats:
                    total_mb = sum(day.get('data', {}).get('volume', 0) for day in stats)
                    print(f"  - Total usage (7 days): {total_mb:.2f} MB")
            except Exception as e:
                print(f"⚠ Usage data retrieval failed (may not have usage data): {e}")

        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        print("\nYou can now run the dashboard with: docker-compose up -d")
        return True

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ API test failed!")
        print("=" * 60)
        print(f"\nError: {str(e)}")
        print("\nPlease check:")
        print("1. Your .env file has correct ONENCE_USERNAME and ONENCE_PASSWORD")
        print("2. Your 1NCE account has API access enabled")
        print("3. Your network connection is working")
        return False


if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
