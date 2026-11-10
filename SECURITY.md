# Security boundaries

This is a single-user local application, not a public server. It binds only `127.0.0.1`; do not put it behind a proxy or expose its port. Any local process with your OS permissions can access your files. The database and exports are plaintext, not a vault.

The API requires a per-process token delivered through the local page, checks Host and Origin, uses no CORS, and does not serve arbitrary files. Responses are no-store with a restrictive CSP. Browser document/model content is rendered as text. SQL is parameterized; imports and merges are transactional. Restores merge instead of replacing existing data.

The token protects against unrelated websites, not a malicious local process or browser extension. The stdlib HTTP server is intended for one trusted local user and has bounded request sizes/timeouts, not internet-scale denial-of-service protection.

The optional inference executable is trusted code chosen by the user. We do not sandbox it by default. It can access whatever your OS allows. The app does not pass shell commands or tool access to a model. Prompt injection can still alter generated answers; source citations are not proof of correctness. No claim is made that answers are safe for high-stakes decisions.

## Reporting

Please do not post private documents or exploitable details in a public issue. If GitHub private vulnerability reporting is available, use the repository's Security tab. Otherwise open an issue asking for a private reporting channel without exploit details; wait for the maintainer's response. No private reporting channel or response-time SLA is currently promised.
