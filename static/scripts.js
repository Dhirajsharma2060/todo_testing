// Fetch tasks on page load
document.addEventListener("DOMContentLoaded", () => {
    fetchTasks();
});

// Fetch tasks from the backend
async function fetchTasks() {
    const response = await fetch("/task");
    const tasks = await response.json();
    tasks.forEach((task) => renderTask(task));
}

// Create a new task
async function createTask() {
    const titleInput = document.getElementById("task-title");
    const title = titleInput.value.trim();
    if (!title) return;

    // Create task on the server
    const response = await fetch("/task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: Date.now(), title, completed: false, status: "todo" }),
    });

    const newTask = await response.json();
    renderTask(newTask);

    titleInput.value = "";
}


// Render a task in the appropriate column
function renderTask(task) {
    const taskElement = document.createElement("div");
    taskElement.classList.add("task");
    taskElement.setAttribute("draggable", "true");
    taskElement.setAttribute("ondragstart", "drag(event)");
    taskElement.setAttribute("id", task.id);
    taskElement.textContent = task.title;

    const containerId = task.status === "in-progress" ? "in-progress-tasks"
                       : task.completed ? "completed-tasks"
                       : "todo-tasks";

    document.getElementById(containerId).appendChild(taskElement);
}

// Allow drag
function allowDrop(event) {
    event.preventDefault();
}

// Handle drag start
function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}

async function drop(event) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData("text");
    const taskElement = document.getElementById(taskId);

    event.target.appendChild(taskElement);

    // Determine new status based on the column it's dropped into
    const newStatus = event.target.id === "in-progress-tasks" ? "in-progress"
                    : event.target.id === "completed-tasks" ? "completed"
                    : "todo";

    // Get task title (assuming taskElement contains the task title)
    const taskTitle = taskElement.textContent;

    // Prepare the completed flag based on newStatus
    const completed = newStatus === "completed";

    // Send update to the backend with all required fields
    const response = await fetch(`/task/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: parseInt(taskId),
            title: taskTitle,
            completed: completed,
            status: newStatus
        }),
    });

    if (!response.ok) {
        console.error("Failed to update task:", await response.json());
    }
}
