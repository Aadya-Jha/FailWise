# Cloudflare Memory Leak Incident (Cloudbleed) (2017)

**Company:** Cloudflare
**Year:** 2017
**Severity:** P0
**Category:** Security vulnerability

## Timeline
On February 18, 2017, Google Project Zero researcher Tavis Ormandy reported a serious memory leak issue affecting Cloudflare edge servers. The vulnerability caused corrupted HTTP responses to leak sensitive memory contents such as cookies, authentication tokens, POST bodies, and API keys. Cloudflare quickly disabled affected features including Email Obfuscation and Automatic HTTPS Rewrites within hours of the report. A full mitigation and deployment of kill switches and patches was completed globally within approximately seven hours. Search engines were also contacted to remove cached leaked data from search indexes.

## Root Cause
The incident was caused by a buffer overrun bug in Cloudflare’s legacy Ragel-based HTML parser. Under specific malformed HTML conditions, a missing `fhold` operation allowed a pointer to move past the end of a memory buffer. This caused memory contents beyond the intended buffer to be included in HTTP responses. The issue remained dormant for years until Cloudflare introduced a newer parser (`cf-html`) that changed internal NGINX buffer behavior, unintentionally activating the vulnerability.

## Resolution
Cloudflare engineers immediately disabled vulnerable parser-dependent features using global kill switches. Additional patches were deployed worldwide to prevent further memory leaks and add stronger pointer safety checks. Cloudflare also worked with major search engines including Google, Bing, and Yahoo to purge cached leaked data from search results. Security teams conducted extensive fuzzing and code reviews to identify similar vulnerabilities in older software components.

## Learnings
Cloudflare identified the risks associated with legacy parser code and began broader audits of older systems for latent security vulnerabilities. The company strengthened parser safety checks, added runtime pointer validation, and improved feature kill switch coverage across all services. The incident also reinforced the importance of aggressive fuzz testing, rapid mitigation systems, and reducing dependency on older low-level parsing implementations.