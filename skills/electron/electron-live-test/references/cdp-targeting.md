# CDP Targeting

Use this reference when an Electron app exposes more than one Chrome DevTools Protocol target or the first target is not the visible renderer.

## Verify Endpoint

```bash
curl --fail --silent http://127.0.0.1:9222/json/version
curl --fail --silent http://127.0.0.1:9222/json/list
```

Use the actual port supplied by the app. The skill's example port is not canonical.

## Select Target

Pick the existing renderer target that matches the visible app window:

- Match by `title` first when the title is app-specific.
- Match by `url` or route when the title is generic.
- Prefer `type: "page"` for renderer UI.
- Avoid `about:blank`, DevTools, extension, service worker, background page, and preload-only targets unless the user asks.

If multiple renderer targets still match, report the candidates and choose the one that best matches the visible window or requested route.

## Do Not Create A New Page

Electron live verification should attach to an existing renderer. A new blank page proves the CDP connection works, but it does not prove the app UI works.

## Security

Treat a non-loopback CDP endpoint as a security issue. Prefer `127.0.0.1:<port>` and avoid exposing remote debugging in packaged or production builds unless explicitly approved.
