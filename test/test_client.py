from clients.api_client import APIClient

class ExercisesClient(APIClient):
    def get_courses_api(self, query):
        return self.get("/api/v1/courses", params=query)


    def get_course_api(self, course_id):
        return self.get(f"/api/v1/courses/{course_id}")


    def create_course_api(self, request):
        return self.post("/api/v1/courses", json=request)


    def update_course_api(self, course_id, request):
        return self.patch(f"/api/v1/courses/{course_id}", json=request)


    def delete_course_api(self, course_id):
        return self.delete(f"/api/v1/courses/{course_id}")


    def get_files_api(self):
        return self.get("/api/v1/files")


    def get_file_api(self, file_id):
        return self.get(f"/api/v1/files/{file_id}")


    def create_file_api(self, request):
        return self.post("/api/v1/files", json=request)


    def delete_file_api(self, file_id):
        return self.delete(f"/api/v1/files/{file_id}")






