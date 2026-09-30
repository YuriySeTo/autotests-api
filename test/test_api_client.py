from clients.api_client import APIClient


class UsersClient(APIClient):
    def create_user_api(self, request):
        return self.post("/api/v1/users", json=request)

    def get_user_api(self, user_id):
        return self.get(f"/api/v1/users/{user_id}")

    def get_user_me_api(self):
        return self.get("/api/v1/users/me")

    def update_user_api(self, user_id, request):
        return self.patch(f"/api/v1/users/{user_id}", json=request)

    def delete_user_api(self, user_id):
        return self.delete(f"/api/v1/users/{user_id}")