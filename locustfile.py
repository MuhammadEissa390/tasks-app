from locust import HttpUser, task, between

class TaskUser(HttpUser):
    wait_time = between(1, 3)  # وقت انتظار عشوائي بين الطلبات

    @task(2)  # الوزن 2: يتم استدعاءه مرتين مقابل كل مرة للـ listTasks
    def add_task(self):
        self.client.post(
            "/addTask",
            json={
                "title": "Test Task",
                "description": "Load testing task",
                "status": "pending"
            }
        )

    @task(1)
    def list_tasks(self):
        self.client.get("/listTasks")

