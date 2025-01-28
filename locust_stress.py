from locust import HttpUser, task

class UsuarioTest(HttpUser):
    @task
    def get_home(self):
        self.client.get("/api/bands") 

    @task
    def post_data(self):
        # Realiza una solicitud POST con un cuerpo de JSON
        self.client.post("/api/bands", json={"name": "value"})  