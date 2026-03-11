from schemas import TaskCreate, TaskUpdate, BaseTask

tasks = []


class TaskService:
    def __init__(self):
        self.task_mock_db = tasks

    def add_task(self, new_task: TaskCreate):

        for task in self.task_mock_db:
            if task.id == new_task.id:
                return None

        self.task_mock_db.append(new_task)

        return BaseTask(**new_task.model_dump())

    def get_all_tasks(self):

        return [
            BaseTask(**task.model_dump())
            for task in self.task_mock_db
        ]

    def get_task(self, task_id: int):

        for task in self.task_mock_db:
            if task.id == task_id:
                return BaseTask(**task.model_dump())

        return None

    def update_task(self, task_id: int, updated_task: TaskUpdate):

        for i, task in enumerate(self.task_mock_db):
            if task.id == task_id:

                update_data = updated_task.model_dump(exclude_unset=True)
                task_data = task.model_dump()

                task_data.update(update_data)

                self.task_mock_db[i] = TaskCreate(**task_data)

                return BaseTask(**task_data)

        return None

    def delete_task(self, task_id: int):

        for task in self.task_mock_db:
            if task.id == task_id:
                self.task_mock_db.remove(task)
                return True

        return False