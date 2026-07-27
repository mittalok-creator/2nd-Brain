# Quick capture on Android

One tap from the home screen to a logged transaction. No opening Notion, no navigating to a
database, no scrolling to `+ New`.

This is the Android equivalent of the iOS Shortcuts flow — a small form that fires a single
API call and closes.

---

## What you actually saw on iOS

The iOS version is **Shortcuts**, Apple's built-in automation app. A shortcut prompts for a
couple of values, calls the Notion API, and dismisses. It can sit in Control Centre, on the
home screen, or in the Today view — which is the "slide down" part.

Android has no built-in equivalent, but it has a better third-party one.

| Approach | Setup | Speed | Notes |
|---|---|---|---|
| **HTTP Shortcuts** | ~15 min, once | Fastest — one tap to a form | Recommended. Free, open source, no account |
| Notion's own widget | 1 min | Slower — lands you in the database | Zero setup, no token. Good fallback |
| Tasker / MacroDroid | 30 min+ | Fast | Overkill unless you already use it |
| Custom web form | Hours | Fast | Needs hosting, and the token would be exposed |

---

## Option A — HTTP Shortcuts *(recommended)*

[HTTP Shortcuts](https://play.google.com/store/apps/details?id=ch.rmy.android.http_shortcuts)
is free and open source. It makes a home-screen icon that shows a small form, then fires an
HTTP request. That is exactly what this needs.

### 1. Create a Notion integration

1. Open <https://www.notion.so/my-integrations> → **New integration**
2. Name it `Android Quick Capture`
3. Copy the **Internal Integration Secret** — this is the token

### 2. Share only the Transactions database with it

Open **💰 Finance → 💸 Transactions** in Notion → `•••` → **Connections** →
add `Android Quick Capture`.

> **Share nothing else.** This token lives on your phone. If the phone is lost, whoever has it
> can reach exactly what you shared and nothing more. Sharing only Transactions is the whole
> point — see [SECURITY.md](../../SECURITY.md) on least privilege.

### 3. Build the shortcut

In HTTP Shortcuts → **+** → **HTTP Shortcut**.

**Basic Request Settings**

| Field | Value |
|---|---|
| Method | `POST` |
| URL | `https://api.notion.com/v1/pages` |

**Request Headers**

| Header | Value |
|---|---|
| `Authorization` | `Bearer YOUR_INTEGRATION_SECRET` |
| `Notion-Version` | `2022-06-28` |
| `Content-Type` | `application/json` |

**Request Body** — type `Custom Text`:

```json
{
  "parent": { "database_id": "bf7b956df0b448c184a87d04a798e3d7" },
  "properties": {
    "Description": { "title": [{ "text": { "content": "{{description}}" } }] },
    "Amount":      { "number": {{amount}} },
    "Direction":   { "select": { "name": "expense" } },
    "Category":    { "select": { "name": "{{category}}" } },
    "Necessity":   { "select": { "name": "{{necessity}}" } },
    "Date":        { "date": { "start": "{{date}}" } }
  }
}
```

`{{amount}}` has **no quotes** — Notion expects a number there, and quoting it fails the request.

### 4. Define the variables

In the app: **Variables** → create four.

| Variable | Type | Configuration |
|---|---|---|
| `amount` | Number Input | Title: "Kitna?" |
| `description` | Text Input | Title: "Kis cheez ka?" |
| `category` | Multiple Choice | Options below |
| `necessity` | Multiple Choice | `essential`, `worthwhile`, `discretionary`, `regretted` |
| `date` | Date | Format `yyyy-MM-dd`, default today |

**Category options** — these must match the Transactions schema exactly:

```
groceries · dining · transport · fuel · health · utilities · housing
subscriptions · shopping · travel · gifts · family · education
insurance · taxes · investment · loan_repayment · other
```

Keep the list short at first. Six or seven you actually use beats eighteen you scroll past —
and you can add more later.

### 5. Put it on the home screen

Long-press the shortcut → **Place on home screen**.

Tap → form appears → amount, what for, category → submit. Two to three seconds.

---

## Why `Necessity` is worth the extra tap

It is tempting to drop it for speed. Don't.

`Amount` and `Category` tell you *where* money went — which you could mostly guess. `Necessity`
tells you how you **felt about it at the time**, before the memory softens.

A month of `regretted` entries in one category is far more actionable than any total, and it is
the one field that cannot be reconstructed later. Two seconds now, or nothing ever.

---

## Option B — Notion's own widget *(no setup, no token)*

If the above feels like too much for now:

1. Long-press the Android home screen → **Widgets** → **Notion**
2. Choose the **Transactions** database
3. Tapping it opens the database with a new row ready

Slower — you fill fields in the Notion UI rather than a compact form — but zero configuration
and no token on the device. A perfectly reasonable starting point; switch to Option A when the
friction starts to show.

---

## Same trick for the Inbox

The highest-volume capture is not transactions, it is thoughts. Duplicate the shortcut with a
simpler body:

```json
{
  "parent": { "database_id": "d4fe90e682f245f29e4d1c6b97e4aab2" },
  "properties": {
    "Content": { "title": [{ "text": { "content": "{{content}}" } }] },
    "Source":  { "select": { "name": "mobile" } },
    "Status":  { "select": { "name": "captured" } }
  }
}
```

One variable, one field, one tap. Share the Inbox database with the same integration.

This matches the capture model deliberately: the inbox asks for one thing and nothing else,
because deciding where something goes is what stops capture from happening
([ADR-0006](../adr/0006-single-inbox-capture.md)).

---

## If it fails

| Response | Cause |
|---|---|
| `401 unauthorized` | Token wrong, or missing the `Bearer ` prefix |
| `404 object_not_found` | Database not shared with the integration — step 2 |
| `400 validation_error` on a property | Property name does not match exactly. They are case-sensitive: `Description`, not `description` |
| `400` on Amount | `{{amount}}` is quoted in the body. Remove the quotes |
| `400` on a select | The option does not exist in the database. Notion will not create select options via the API |

HTTP Shortcuts shows the full response on failure — read it, the message names the offending
property.

---

## Not yet verified

This configuration is written from the Notion API contract and the deployed schema, but has
**not been run end to end from a device** — that needs a token, which belongs on your phone and
not in this repository.

If a step is wrong, the error table above should identify it. Report what the response says and
it can be corrected.
