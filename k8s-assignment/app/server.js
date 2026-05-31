const express = require('express');
const mongoose = require('mongoose');

const app = express();
const PORT = 3000;

// MongoDB connection using environment variable
const MONGO_URL = process.env.MONGO_URL || 'mongodb://localhost:27017/tododb';

mongoose.connect(MONGO_URL)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

// Todo schema
const todoSchema = new mongoose.Schema({
  task: { type: String, required: true },
  createdAt: { type: Date, default: Date.now }
});
const Todo = mongoose.model('Todo', todoSchema);

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Main page - list all todos
app.get('/', async (req, res) => {
  const todos = await Todo.find().sort({ createdAt: -1 });
  let listItems = todos.map(t =>
    `<li style="padding:8px 0; border-bottom:1px solid #eee;">
      ${t.task}
      <form action="/delete/${t._id}" method="POST" style="display:inline; margin-left:10px;">
        <button type="submit" style="background:#e74c3c;color:white;border:none;padding:3px 8px;border-radius:3px;cursor:pointer;">Delete</button>
      </form>
    </li>`
  ).join('');

  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Todo App - Kubernetes Demo</title>
      <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 0 20px; }
        h1 { color: #2c3e50; }
        input[type="text"] { width: 70%; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 4px; }
        button[type="submit"] { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        ul { list-style: none; padding: 0; }
        .badge { background: #27ae60; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
      </style>
    </head>
    <body>
      <h1>Todo List <span class="badge">Running on Kubernetes</span></h1>
      <form action="/add" method="POST" style="margin-bottom: 20px;">
        <input type="text" name="task" placeholder="Enter a new task..." required />
        <button type="submit">Add</button>
      </form>
      <ul>${listItems || '<li>No tasks yet. Add one above!</li>'}</ul>
      <p style="color:#999; font-size:12px;">Total tasks: ${todos.length}</p>
    </body>
    </html>
  `);
});

// Add a new todo
app.post('/add', async (req, res) => {
  const { task } = req.body;
  if (task && task.trim()) {
    await Todo.create({ task: task.trim() });
  }
  res.redirect('/');
});

// Delete a todo
app.post('/delete/:id', async (req, res) => {
  await Todo.findByIdAndDelete(req.params.id);
  res.redirect('/');
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date() });
});

app.listen(PORT, () => {
  console.log(`Todo app running on port ${PORT}`);
});
