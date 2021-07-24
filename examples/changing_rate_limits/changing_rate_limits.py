from blitzcrank import Blitzcrank
import time

# Default rate limits are inline with those for Developer API keys
# - 20 requests every 1 second(s)
# - 100 requests every 2 minute(s)
b = Blitzcrank("RGAPI-10ec71d4-32b7-464b-a75d-9ce28708f6c7", "euw1")

# When you have an app that is approved, you may have limits like the following
# - 500 requests every 10 second(s)
# - 30000 requests every 10 minute(s)
b.change_rate_limits(500, 10, 30000, 600)

request_times = []

for call in range(101):
    start_time = time.time()

    account_id = b.summoner.get_account_id("Thebausffs")

    runtime = time.time() - start_time
    print(account_id, call, str(runtime)+"s")
    request_times.append(runtime)

# Rate limiting within Blitzcrank waits by default if cap is hit,
# so requests over the set limit will wait the applicable call_period duration
verify_request_times = not bool(sum([time > 1 for time in request_times]))
print(f"All requests within budget: {verify_request_times}")
