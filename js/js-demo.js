/* =========================================================
   JavaScript page interactions: counter / RGB color picker / to-do list
   ========================================================= */
(function () {
  "use strict";

  /* ---------- Demo 1: counter ---------- */
  let count = 0;
  const counterDisplay = document.getElementById("counterDisplay");

  function renderCounter() {
    counterDisplay.textContent = count;
  }
  const plusBtn = document.getElementById("plusBtn");
  if (plusBtn) {
    plusBtn.addEventListener("click", function () {
      count += 1;
      renderCounter();
    });
    document.getElementById("minusBtn").addEventListener("click", function () {
      count -= 1;
      renderCounter();
    });
    document.getElementById("resetBtn").addEventListener("click", function () {
      count = 0;
      renderCounter();
    });
  }

  /* ---------- Demo 2: RGB color picker ---------- */
  const rRange = document.getElementById("rRange");
  if (rRange) {
    const gRange = document.getElementById("gRange");
    const bRange = document.getElementById("bRange");
    const swatch = document.getElementById("colorSwatch");

    function renderColor() {
      const r = parseInt(rRange.value, 10);
      const g = parseInt(gRange.value, 10);
      const b = parseInt(bRange.value, 10);
      const rgb = "rgb(" + r + ", " + g + ", " + b + ")";
      swatch.style.background = rgb;
      swatch.textContent = rgb;
      document.getElementById("rVal").textContent = r;
      document.getElementById("gVal").textContent = g;
      document.getElementById("bVal").textContent = b;
    }
    [rRange, gRange, bRange].forEach(function (input) {
      input.addEventListener("input", renderColor);
    });
  }

  /* ---------- Demo 3: to-do list (in-memory state, cleared on refresh) ---------- */
  const todoText = document.getElementById("todoText");
  const addTodo = document.getElementById("addTodo");
  const todoList = document.getElementById("todoList");
  const todoEmpty = document.getElementById("todoEmpty");
  let todos = [];

  function renderTodos() {
    // Remove existing tasks except the empty-state placeholder
    todoList.querySelectorAll("li").forEach(function (li) {
      if (li !== todoEmpty) li.remove();
    });

    if (todos.length === 0) {
      todoEmpty.style.display = "block";
      return;
    }
    todoEmpty.style.display = "none";

    todos.forEach(function (todo, index) {
      const li = document.createElement("li");
      if (todo.done) li.classList.add("done");

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = todo.done;
      checkbox.setAttribute("aria-label", "Mark as done");
      checkbox.addEventListener("change", function () {
        todos[index].done = this.checked;
        renderTodos();
      });

      const span = document.createElement("span");
      span.textContent = todo.text;

      const del = document.createElement("button");
      del.textContent = "✕";
      del.setAttribute("aria-label", "Delete");
      del.addEventListener("click", function () {
        todos.splice(index, 1);
        renderTodos();
      });

      li.appendChild(checkbox);
      li.appendChild(span);
      li.appendChild(del);
      todoList.appendChild(li);
    });
  }

  function addTask() {
    const text = todoText.value.trim();
    if (!text) {
      todoText.focus();
      return;
    }
    todos.push({ text: text, done: false });
    todoText.value = "";
    renderTodos();
    todoText.focus();
  }

  if (addTodo) {
    addTodo.addEventListener("click", addTask);
    todoText.addEventListener("keydown", function (e) {
      if (e.key === "Enter") addTask();
    });
  }
})();
