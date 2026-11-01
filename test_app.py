import unittest

from app import create_app


class TaskApiTests(unittest.TestCase):
    def setUp(self):
        # Fresh app (and empty store) for every test
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_health(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {"status": "ok"})

    def test_create_task(self):
        res = self.client.post("/tasks", json={"title": "Write tests"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(
            res.get_json(), {"id": 1, "title": "Write tests", "done": False}
        )

    def test_create_task_requires_title(self):
        res = self.client.post("/tasks", json={})
        self.assertEqual(res.status_code, 400)
        self.assertIn("title", res.get_json()["error"])

    def test_list_tasks(self):
        self.client.post("/tasks", json={"title": "A"})
        self.client.post("/tasks", json={"title": "B"})
        res = self.client.get("/tasks")
        self.assertEqual(res.status_code, 200)
        self.assertEqual([t["title"] for t in res.get_json()], ["A", "B"])

    def test_get_task_not_found(self):
        res = self.client.get("/tasks/999")
        self.assertEqual(res.status_code, 404)

    def test_update_task(self):
        self.client.post("/tasks", json={"title": "Old"})
        res = self.client.put("/tasks/1", json={"title": "New", "done": True})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {"id": 1, "title": "New", "done": True})

    def test_delete_task(self):
        self.client.post("/tasks", json={"title": "Temp"})
        self.assertEqual(self.client.delete("/tasks/1").status_code, 204)
        self.assertEqual(self.client.get("/tasks/1").status_code, 404)


if __name__ == "__main__":
    unittest.main()