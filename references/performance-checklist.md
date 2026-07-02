# Performance Checklist

> Performance targets and measurement. Pulled in by /review (performance persona).

## Core Web Vitals (frontend)

| Metric | Target | Good | Needs improvement |
|---|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | < 2.5s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | < 200ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | < 0.1 | > 0.25 |
| FCP (First Contentful Paint) | < 1.8s | < 1.8s | > 3.0s |
| TTFB (Time to First Byte) | < 800ms | < 800ms | > 1.8s |

## Frontend checklist

### Loading
- [ ] Images optimized (WebP/AVIF, lazy-loaded, responsive `srcset`).
- [ ] JavaScript bundled and minified.
- [ ] CSS bundled and minified.
- [ ] Critical CSS inlined (above-the-fold).
- [ ] Non-critical resources deferred or async.
- [ ] Fonts preloaded, `font-display: swap`.
- [ ] HTTP/2 or HTTP/3 enabled.

### Rendering
- [ ] No layout thrashing (read-then-write DOM).
- [ ] Virtualized lists for 100+ items.
- [ ] Memoized expensive components (`React.memo`, `useMemo`).
- [ ] Debounced/throttled scroll and resize handlers.
- [ ] No synchronous layout recalcs in loops.

### Bundle
- [ ] Bundle size < 200KB gzipped (initial load).
- [ ] Code splitting for route-level chunks.
- [ ] Tree shaking enabled.
- [ ] No unused dependencies in bundle.
- [ ] Analyzed with `webpack-bundle-analyzer` or equivalent.

## Backend checklist

### Database
- [ ] N+1 queries eliminated (use joins, includes, eager loading).
- [ ] Indexes on columns used in WHERE, JOIN, ORDER BY.
- [ ] Query results paginated (no unbounded SELECT).
- [ ] Slow query log monitored (queries > 100ms).
- [ ] Connection pooling configured.

### API
- [ ] Response payloads minimal (no over-fetching).
- [ ] Compression enabled (gzip/brotli).
- [ ] Caching headers set (Cache-Control, ETag).
- [ ] Rate limiting configured.
- [ ] Timeouts on external calls.

### Memory
- [ ] No memory leaks (check with long-running tests).
- [ ] Large objects released (not held in scope).
- [ ] Streams used for large data (not buffered in memory).

### Concurrency
- [ ] Async I/O for network/disk operations.
- [ ] No blocking calls on the main thread/event loop.
- [ ] Connection/thread pools sized correctly.

## Measurement commands

```bash
# Frontend
npx lighthouse <url> --view  # Lighthouse audit
npx @arethetypeswrong/cli    # Bundle size check

# Backend
# Node.js
node --prof <script> && node --prof-process isolate-*.log
# Python
python -m cProfile -s time <script>
# Go
go test -bench=. -benchmem
# Database
EXPLAIN ANALYZE <query>  # PostgreSQL
```

## Anti-patterns

- **Premature optimization**: Optimizing without profiling. Measure first.
- **N+1 queries**: Loading a list, then querying each item's related data.
- **Synchronous I/O on event loop**: Blocks all other requests.
- **Unbounded queries**: `SELECT * FROM table` with no LIMIT.
- **Missing indexes**: Queries scanning full tables.
- **Over-fetching**: Returning 50 fields when the client needs 3.
- **No pagination**: Loading 10,000 records at once.
- **Layout thrashing**: `offsetHeight` then `style.height` in a loop.
- **Giant bundles**: 1MB+ initial JavaScript load.

## Red Flags
- API response > 100KB (unless intentionally large).
- Database query > 100ms.
- Frontend bundle > 200KB gzipped.
- LCP > 4s.
- Memory usage growing over time (leak).
- No caching headers on static assets.
- Synchronous I/O in async context.
