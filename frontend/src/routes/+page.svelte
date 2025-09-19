<script lang="ts">
    import { onMount } from "svelte";

    interface TODO {
        title: string
        id: number
        done: boolean
    }

    let todos: TODO[] = $state([]);
    let newTodo: string = $state("");

    const API_URL: string = "http://127.0.0.1:8000";

    async function loadTodos() {
        const res = await fetch(`${API_URL}/todos`);
        todos = await res.json() as TODO[];
    }

    async function addTodo() {
        if (!newTodo.trim()) return;
        const res = await fetch(`${API_URL}/todos`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: newTodo, completed: false })
        });
        const todo = await res.json() as TODO;
        todos = [...todos, todo];
        newTodo = "";
    }

    async function toggleTodo(todo: TODO) {
        const updated: TODO = { ...todo, done: !todo.done };
        await fetch(`${API_URL}/todos/${todo.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updated)
        });
        todos = todos.map(t => t.id === todo.id ? updated : t);
    }

    async function deleteTodo(id: number) {
        await fetch(`${API_URL}/todos/${id}`, { method: "DELETE" });
        todos = todos.filter(t => t.id !== id);
    }

    onMount(loadTodos);
</script>

<div class="max-w-md mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">ToDo List</h1>

    <div class="flex gap-2 mb-4">
        <input
            bind:value={newTodo}
            placeholder="New task..."
            class="flex-1 border rounded px-2 py-1"
        />
        <button
            onclick={addTodo}
            class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
        >
            Add
        </button>
    </div>

    <ul class="space-y-2">
        {#each todos as todo}
            <li class="flex items-center justify-between border-b pb-1">
                <label class="flex items-center gap-2 cursor-pointer">
                    <input
                        type="checkbox"
                        checked={todo.done}
                        onchange={() => toggleTodo(todo)}
                    />
                    <span class:line-through={todo.done}>{todo.title}</span>
                </label>
                <button
                    onclick={() => deleteTodo(todo.id)}
                    class="text-red-500 hover:underline"
                >
                    Delete
                </button>
            </li>
        {/each}
    </ul>
</div>

<style>
    .line-through {
        text-decoration: line-through;
    }
</style>
