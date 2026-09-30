# Run-log signatures

Four signatures, each from a failure that actually happened.

| Signature | Why it is a defect | What it looked like |
| --- | --- | --- |
| A **control-plane write to a non-local or placeholder host** | The write went nowhere, `curl` exited 0, and the run reported success | `PUT https://paperclip-api.example.com/api/status-cards/…` — the card sat `compiling` for an hour |
| A Paperclip API call with **no `-f`/`%{http_code}` and no read-back** | Unreachable host, 400 and 200 all exit 0; the run is reporting a belief | every seat that "updated" a card it never checked |
| A **tool error swallowed mid-run** | The run continued as if it had not happened, so the output is built on a gap | `"status":"error"` inside a `tool_use` part |
| A run that produced **one or two lines** | Started and died — capacity spent, nothing produced | 30 of 195 runs in one day |
