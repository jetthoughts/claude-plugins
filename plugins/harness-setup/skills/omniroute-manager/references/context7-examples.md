# Context7 Query Patterns

## Search → Fetch Workflow

```bash
# 1. Search for library
curl -s "https://context7.com/api/v2/libs/search?libraryName=<LIB>&query=<TOPIC>" | jq '.results[0]'

# 2. Fetch docs using returned ID
curl -s "https://context7.com/api/v2/context?libraryId=<ID>&query=<TOPIC>&type=txt"
```

---

## Common Libraries & IDs

| Library | Search Query | Typical ID |
|---------|--------------|------------|
| React | `react hooks` | `/websites/react_dev_reference` |
| Next.js | `nextjs routing` | `/vercel/next.js` |
| FastAPI | `fastapi dependencies` | `/fastapi/fastapi` |
| TypeScript | `typescript types` | `/microsoft/typescript` |
| Node.js | `node fs` | `/nodejs/node` |
| Python | `python asyncio` | `/python/cpython` |
| Go | `go http` | `/golang/go` |
| Rust | `rust tokio` | `/tokio-rs/tokio` |
| Vue | `vue composition api` | `/vuejs/vue` |
| Svelte | `svelte stores` | `/sveltejs/svelte` |
| Tailwind | `tailwind utilities` | `/tailwindlabs/tailwindcss` |
| Prisma | `prisma schema` | `/prisma/prisma` |
| Drizzle | `drizzle relations` | `/drizzle-team/drizzle-orm` |
| Zod | `zod schema` | `/colinhacks/zod` |
| tRPC | `trpc router` | `/trpc/trpc` |
| Bun | `bun test` | `/oven-sh/bun` |
| Deno | `deno kv` | `/denoland/deno` |

---

## Query Tips

- **Be specific:** `useState` better than `hooks`
- **Use type=txt:** Returns plain text, more readable than JSON
- **Check totalSnippets:** If 0, library not indexed or query too narrow
- **Broaden if empty:** Remove query param, just use libraryName

---

## Example Sessions

### React useEffect cleanup
```bash
curl -s "https://context7.com/api/v2/libs/search?libraryName=react&query=useEffect cleanup" | jq '.results[0].id'
curl -s "https://context7.com/api/v2/context?libraryId=/websites/react_dev_reference&query=useEffect cleanup&type=txt"
```

### Next.js Server Actions
```bash
curl -s "https://context7.com/api/v2/libs/search?libraryName=nextjs&query=server actions" | jq '.results[0].id'
curl -s "https://context7.com/api/v2/context?libraryId=/vercel/next.js&query=server+actions&type=txt"
```

### FastAPI Background Tasks
```bash
curl -s "https://context7.com/api/v2/libs/search?libraryName=fastapi&query=background tasks" | jq '.results[0].id'
curl -s "https://context7.com/api/v2/context?libraryId=/fastapi/fastapi&query=background+tasks&type=txt"
```

### Prisma Many-to-Many
```bash
curl -s "https://context7.com/api/v2/libs/search?libraryName=prisma&query=many to many" | jq '.results[0].id'
curl -s "https://context7.com/api/v2/context?libraryId=/prisma/prisma&query=many-to-many&type=txt"
```

### Zod Discriminated Unions
```bash
curl -s "https://context7.com/api/v2/libs/search?libraryName=zod&query=discriminated union" | jq '.results[0].id'
curl -s "https://context7.com/api/v2/context?libraryId=/colinhacks/zod&query=discriminated+union&type=txt"
```

### tRPC v11 Router
```bash
curl -s "https://context7.com/api/v2/libs/search?libraryName=trpc&query=router v11" | jq '.results[0].id'
curl -s "https://context7.com/api/v2/context?libraryId=/trpc/trpc&query=router&type=txt"
```

---

## Helper Script

```bash
# omni-context7.sh <library> <query>
# Already bundled in scripts/
./scripts/omni-context7.sh react useEffect
./scripts/omni-context7.sh nextjs "app router"
./scripts/omni-context7.sh fastapi "dependency injection"
```