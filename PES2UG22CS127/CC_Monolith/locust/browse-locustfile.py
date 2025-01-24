from locust import task, run_single_user, FastHttpUser


class Browse(FastHttpUser):
    host = "http://localhost:5000"

    # Default headers that are common for all requests
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
    }

    @task
    def browse_page(self):
        """
        Simulate browsing the page by sending a GET request to /browse.
        """
        headers = self.default_headers.copy()
        headers["Host"] = "localhost:5000"
        headers["Priority"] = "u=0, i"
        
        with self.client.get("/browse", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to browse page. Status code: {response.status_code}")


if __name__ == "__main__":
    run_single_user(Browse)
