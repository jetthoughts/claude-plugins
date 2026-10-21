export const meta = {
  name: 'j-perplexity-sync',
  description: 'Sync Perplexity library threads into the vault via BrowserOS — idempotent, watermark-based, with artifact collection',
  phases: [
    { title: 'Setup', detail: 'Read hub, start BrowserOS session' },
    { title: 'Library', detail: 'Scrape library page for thread UUIDs in window' },
    { title: 'Filter', detail: 'Dedupe against hub, partition by kind' },
    { title: 'Fetch', detail: 'Fetch thread panes in batches of 3' },
    { title: 'Artifacts', detail: 'Collect artifacts for threads that name saved documents' },
    { title: 'Write', detail: 'Write inbox files with frontmatter' },
    { title: 'Normalize', detail: 'Run normalizer, commit, report' },
  ],
}

const args = globalThis.args || {}
const WINDOW = args.window || 'last 7 days'
const VAULT_ROOT = '/Users/pftg/dev/pkm'
const INBOX_DIR = VAULT_ROOT + '/research/_inbox/perplexity'
const HUB_PATH = VAULT_ROOT + '/evidence/perplexity/perplexity-library.md'
const NORMALIZER = '/Users/pftg/.claude/skills/j-inbox/scripts/normalize.py'

phase('Setup')

const hubResult = await agent('Read file ' + HUB_PATH + ' and return content as plain text.', { label: 'read-hub', phase: 'Setup' })
const knownIds = [...hubResult.matchAll(/pplx-([0-9a-f]{8})/g)].map(m => m[1])
log('Hub has ' + knownIds.length + ' known IDs')

phase('Library')

const libraryResult = await agent(
  'Scrape https://www.perplexity.ai/library with BrowserOS. Scroll to load all rows. For each main [role="row"], walk __reactFiber props (≤6 parents), regex /(search|computer\\/tasks)/<uuid>. Row age = last cell. Return JSON array [{uuid, age, title}] for rows in window "' + WINDOW + '". Use tabs new+background, run for scroll+extract, close tab.',
  { label: 'scrape-library', phase: 'Library' }
)
const libraryData = typeof libraryResult === 'string' ? JSON.parse(libraryResult) : libraryResult
log('Extracted ' + libraryData.length + ' threads from library')

phase('Filter')

const filtered = libraryData.filter(t => !knownIds.includes(t.uuid.slice(0, 8)))
log('After window filter & dedupe: ' + filtered.length + ' new threads')

const byKind = { search: [], 'computer-task': [] }
for (const t of filtered) {
  byKind[t.uuid.includes('computer') ? 'computer-task' : 'search'].push(t)
}

log('Search: ' + byKind.search.length + ', Computer-task: ' + byKind['computer-task'].length)

phase('Fetch')

const fetched = []

for (const kind of ['search', 'computer-task']) {
  const items = byKind[kind]
  for (let i = 0; i < items.length; i += 3) {
    const batch = items.slice(i, i + 3)
    const results = await parallel(batch.map(t => () => agent(
      `Fetch Perplexity ${kind} ${t.uuid.slice(0,8)}. Open https://www.perplexity.ai/${kind === 'search' ? 'search' : 'computer/tasks'}/${t.uuid} in BrowserOS bg tab. Wait 5.5s. Read main as markdown. If <500 chars, wait 4s, re-read no selector. Strip UNTRUSTED_PAGE_CONTENT. Extract date from "Sep 2, 5:01 PM", title from H1 or first 60 chars of query, project from "[<Project>/" prefix. Return JSON {uuid, url, date, title, project, body, kind}. Close tab.`,
      { label: 'fetch-' + t.uuid.slice(0, 8), phase: 'Fetch', schema: {
        type: 'object',
        properties: {
          uuid: { type: 'string' },
          url: { type: 'string' },
          date: { type: 'string' },
          title: { type: 'string' },
          project: { type: 'string' },
          body: { type: 'string' },
          kind: { type: 'string' },
        },
        required: ['uuid', 'url', 'date', 'title', 'project', 'body', 'kind']
      }}
    )))
    fetched.push(...results.filter(Boolean))
    if (i + 3 < items.length) await new Promise(r => setTimeout(r, 2000))
  }
}

log('Fetched ' + fetched.length + ' thread panes')

phase('Artifacts')

const artifactThreads = fetched.filter(t =>
  t.body.includes('Saved and attached') ||
  t.body.includes('Generated Document') ||
  t.body.includes('saved document')
)
log(artifactThreads.length + ' threads reference artifacts')

let artifactCount = 0
const docNames = artifactThreads.flatMap(t => {
  const names = []
  for (const p of [
    /Saved and attached[:\s]*([^\n]+)/gi,
    /Generated Document[:\s]*([^\n]+)/gi,
    /saved document[:\s]*([^\n]+)/gi
  ]) {
    let m
    while ((m = p.exec(t.body)) !== null) names.push(m[1].trim())
  }
  return [...new Set(names)].map(n => ({ threadId: t.uuid, docName: n }))
})

if (docNames.length > 0) {
  const artifactResult = await agent(
    `Collect Perplexity artifacts. Open https://www.perplexity.ai/computer/artifacts in BrowserOS. Scroll to bottom until all month groups rendered. For ${docNames.length} doc names (in workflow scope): find card matching docName, open Artifact options, Open session, verify task id matches threadId. Download matching cards. Return count. Use tabs, run, act.`,
    { label: 'collect-artifacts', phase: 'Artifacts' }
  )
  artifactCount = parseInt(artifactResult) || 0
}

log('Downloaded ' + artifactCount + ' artifacts')

phase('Write')

const writeDataPath = '/tmp/perplexity-write-data.json'
await agent('Write ' + writeDataPath + ' with JSON of ' + JSON.stringify(fetched) + '. Use fs.writeFileSync.', { label: 'write-data', phase: 'Write' })

await agent(
  'Read ' + writeDataPath + '. Create ' + INBOX_DIR + ' if needed. For each thread: write <uuid>.md with frontmatter: source: perplexity, source_id: <uuid>, url, date, title (double-quoted), project. Body = thread.body. YAML --- delimiters.',
  { label: 'write-inbox', phase: 'Write' }
)
log('Wrote ' + fetched.length + ' inbox files')

phase('Normalize')

await agent('Run: cd ' + VAULT_ROOT + ' && python3 ' + NORMALIZER + ' ingest. Return stdout.', { label: 'normalize', phase: 'Normalize' })
log('Normalizer done')

await agent('Run: cd ' + VAULT_ROOT + ' && git add -A && git commit -m "Sync Perplexity: ' + fetched.length + ' threads" || true. Return stdout.', { label: 'commit', phase: 'Normalize' })
log('Commit done')

return {
  synced: fetched.length,
  skipped: libraryData.length - filtered.length,
  artifacts: artifactCount,
  citations_preserved: fetched.filter(t => t.body.includes('[')).length,
}