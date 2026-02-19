import React, { useEffect, useState } from "react";
import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

function App() {
  const [machines, setMachines] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);

  const [machineForm, setMachineForm] = useState({
    name: "",
    location: "",
    description: "",
  });

  const [taskForm, setTaskForm] = useState({
    title: "",
    description: "",
    due_date: "",
  });

  const loadMachines = async () => {
    setLoading(true);
    try {
      const res = await api.get("/machines/");
      setMachines(res.data);
      if (!selectedMachine && res.data.length > 0) {
        setSelectedMachine(res.data[0]);
      }
    } finally {
      setLoading(false);
    }
  };

  const loadTasks = async (machineId) => {
    if (!machineId) return;
    setLoading(true);
    try {
      const res = await api.get("/tasks/", {
        params: { machine_id: machineId },
      });
      setTasks(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMachines();
  }, []);

  useEffect(() => {
    if (selectedMachine) {
      loadTasks(selectedMachine.id);
    } else {
      setTasks([]);
    }
  }, [selectedMachine]);

  const handleMachineSubmit = async (e) => {
    e.preventDefault();
    await api.post("/machines/", machineForm);
    setMachineForm({ name: "", location: "", description: "" });
    await loadMachines();
  };

  const handleTaskSubmit = async (e) => {
    e.preventDefault();
    if (!selectedMachine) return;
    await api.post("/tasks/", {
      ...taskForm,
      machine_id: selectedMachine.id,
      due_date: new Date(taskForm.due_date).toISOString(),
    });
    setTaskForm({ title: "", description: "", due_date: "" });
    await loadTasks(selectedMachine.id);
  };

  const handleTaskStatusChange = async (taskId, status) => {
    await api.put(`/tasks/${taskId}`, { status });
    await loadTasks(selectedMachine.id);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Machine Maintenance Scheduler</h1>
      </header>

      <main className="layout">
        <section className="panel">
          <h2>Machines</h2>
          {loading && <p className="muted">Loading...</p>}
          <ul className="list">
            {machines.map((m) => (
              <li
                key={m.id}
                className={
                  selectedMachine && selectedMachine.id === m.id
                    ? "list-item selected"
                    : "list-item"
                }
                onClick={() => setSelectedMachine(m)}
              >
                <div className="list-item-title">{m.name}</div>
                <div className="list-item-sub">
                  {m.location || "No location"} ·{" "}
                  {m.is_active ? "Active" : "Inactive"}
                </div>
              </li>
            ))}
          </ul>

          <h3>Add Machine</h3>
          <form className="form" onSubmit={handleMachineSubmit}>
            <input
              type="text"
              placeholder="Name"
              value={machineForm.name}
              onChange={(e) =>
                setMachineForm({ ...machineForm, name: e.target.value })
              }
              required
            />
            <input
              type="text"
              placeholder="Location"
              value={machineForm.location}
              onChange={(e) =>
                setMachineForm({ ...machineForm, location: e.target.value })
              }
            />
            <textarea
              placeholder="Description"
              value={machineForm.description}
              onChange={(e) =>
                setMachineForm({
                  ...machineForm,
                  description: e.target.value,
                })
              }
            />
            <button type="submit">Create Machine</button>
          </form>
        </section>

        <section className="panel">
          <h2>
            Tasks{" "}
            {selectedMachine ? `for ${selectedMachine.name}` : "(no machine selected)"}
          </h2>

          <ul className="list">
            {tasks.map((t) => (
              <li key={t.id} className="list-item">
                <div className="list-item-title">{t.title}</div>
                <div className="list-item-sub">
                  Due: {new Date(t.due_date).toLocaleString()} · Status:{" "}
                  <strong>{t.status}</strong>
                </div>
                <div className="pill-row">
                  {["scheduled", "in_progress,completed", "cancelled"] && null}
                  {["scheduled", "in_progress", "completed", "cancelled"].map(
                    (status) => (
                      <button
                        key={status}
                        type="button"
                        className={
                          t.status === status ? "pill active" : "pill"
                        }
                        onClick={() => handleTaskStatusChange(t.id, status)}
                      >
                        {status}
                      </button>
                    ),
                  )}
                </div>
              </li>
            ))}
            {tasks.length === 0 && (
              <li className="muted">No tasks for this machine yet.</li>
            )}
          </ul>

          {selectedMachine && (
            <>
              <h3>Schedule Task</h3>
              <form className="form" onSubmit={handleTaskSubmit}>
                <input
                  type="text"
                  placeholder="Title"
                  value={taskForm.title}
                  onChange={(e) =>
                    setTaskForm({ ...taskForm, title: e.target.value })
                  }
                  required
                />
                <textarea
                  placeholder="Description"
                  value={taskForm.description}
                  onChange={(e) =>
                    setTaskForm({
                      ...taskForm,
                      description: e.target.value,
                    })
                  }
                />
                <input
                  type="datetime-local"
                  value={taskForm.due_date}
                  onChange={(e) =>
                    setTaskForm({ ...taskForm, due_date: e.target.value })
                  }
                  required
                />
                <button type="submit">Create Task</button>
              </form>
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;

