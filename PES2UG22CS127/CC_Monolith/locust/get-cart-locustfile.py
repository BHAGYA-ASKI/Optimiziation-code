from locust import task, run_single_user, FastHttpUser
from insert_product import login

class AddToCartUser(FastHttpUser):
    host = "http://localhost:5000"
    username = "test123"
    password = "test123"
    
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
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    def on_start(self):
        """
        Called when a simulated user starts running.
        Logs in and retrieves the authentication token.
        """
        try:
            cookies = login(self.username, self.password)
            self.token = cookies.get("token")
            if not self.token:
                raise ValueError("Failed to get token, login unsuccessful.")
        except Exception as e:
            print(f"Error during login: {e}")
            self.token = None

    @task
    def view_cart(self):
        """
        Simulate a GET request to view the cart.
        """
        if self.token:
            headers = self.default_headers.copy()
            headers["Cookie"] = f"token={self.token}"
            headers["Referer"] = "http://localhost:5000/product/1"
            
            with self.client.get("/cart", headers=headers, catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed to fetch cart. Status code: {response.status_code}")
        else:
            print("Skipping cart view. No valid token.")

if __name__ == "__main__":
    run_single_user(AddToCartUser)
