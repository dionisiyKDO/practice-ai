# Practice-ai

## Backend

```sh
cd backend
uv run uvicorn main:app --reload
```

## Frontend

```sh
cd frontend
bun run dev
```

## ChatGPT

Chat link: `https://chatgpt.com/share/68cc528e-1fd4-8003-9192-40569a1634d8`

First version message - FastAPI code
Third version message - Svelte5 code

FastAPI didn't change at all
Svelte:
    - added typescript interface
    - added typescript type checking
    - adapted naming from two different message contexts (todo.completed to todo.done)
    - Deleted cringe emoji
    - fixed Svelte4 syntax(Svelte5 introduced runes, $state() in particular, and changed syntax for binding clicking events (from on:click to onclick) )
