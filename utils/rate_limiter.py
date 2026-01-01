import time
from datetime import datetime, timedelta

class RateLimiter:
    """
    Rate limiter to prevent exceeding Gemini API quotas
    Gemini Free Tier: 15 requests per minute (RPM)
    """
    
    def __init__(self, max_requests_per_minute=10):
        """
        Initialize rate limiter
        Set to 10 RPM to be safe (Gemini free tier allows 15 RPM)
        """
        self.max_requests = max_requests_per_minute
        self.time_window = 60  # seconds
        self.request_times = []  # Use instance variable instead of session state
    
    def can_make_request(self):
        """Check if we can make another API request"""
        current_time = datetime.now()
        
        # Remove requests older than time window
        self.request_times = [
            req_time for req_time in self.request_times
            if current_time - req_time < timedelta(seconds=self.time_window)
        ]
        
        # Check if under limit
        return len(self.request_times) < self.max_requests
    
    def record_request(self):
        """Record that an API request was made"""
        self.request_times.append(datetime.now())
    
    def wait_if_needed(self):
        """
        Wait if we've hit the rate limit
        Returns: seconds waited (0 if no wait needed)
        """
        if not self.can_make_request():
            # Calculate wait time
            oldest_request = min(self.request_times)
            wait_until = oldest_request + timedelta(seconds=self.time_window)
            wait_seconds = (wait_until - datetime.now()).total_seconds()
            
            if wait_seconds > 0:
                print(f"⏳ Rate limit reached. Waiting {int(wait_seconds)} seconds...")
                time.sleep(wait_seconds + 1)  # Add 1 second buffer
                return wait_seconds
        
        return 0
    
    def get_remaining_requests(self):
        """Get number of requests remaining in current window"""
        current_time = datetime.now()
        
        # Clean old requests
        self.request_times = [
            req_time for req_time in self.request_times
            if current_time - req_time < timedelta(seconds=self.time_window)
        ]
        
        return self.max_requests - len(self.request_times)
    
    def get_reset_time(self):
        """Get time until rate limit resets"""
        if not self.request_times:
            return 0
        
        oldest_request = min(self.request_times)
        reset_time = oldest_request + timedelta(seconds=self.time_window)
        seconds_until_reset = (reset_time - datetime.now()).total_seconds()
        
        return max(0, seconds_until_reset)

# Global rate limiter instance
gemini_rate_limiter = RateLimiter(max_requests_per_minute=10)