"""Generate IVO OS V03 prototype into v3/. Run: python3 gen_v3.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen3"))
import con_b, customer, contractor, pages
con_b.build(); customer.build_customer(); customer.build_portal()
contractor.build_contractor(); contractor.build_vendor()
pages.build_apply(); pages.build_onboarding(); pages.build_hub()
print("V03 built")
