<p align="center">
  <img src="header.png" alt="Abraxas Labs — gitea-hostmatcher-0000-ssrf" width="100%">
</p>

<p align="center">
  <a href="https://abraxaslabs.tech"><strong>abraxaslabs.tech</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas">github.com/abraxas</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas/gitea-hostmatcher-0000-ssrf">gitea-hostmatcher-0000-ssrf</a>
</p>

# gitea-hostmatcher-0000-ssrf

**Gitea** `1.27.3` — Gitea

Unpublished Gitea source finding: hostmatcher residual SSRF via 0.0.0.0/8.

| | |
|---|---|
| ID | Unpublished Gitea source finding #3 (no CVE yet) |
| CWE | [CWE-918](https://cwe.mitre.org/data/definitions/918.html) |
| CVSS | **High: 7.7** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Product | [Gitea](https://github.com/go-gitea/gitea) |
| Affected | all versions **through 1.27.3** (inclusive) |
| Patched | vendor patch — see references |
| Auth | authenticated (see source map) |
| License | [GNU Affero GPL v3.0](LICENSE) |
| Lab | `127.0.0.1` only · vendor/client disclosure pack, not a scanner |

---

## Advisory (from the source map)

modules/hostmatcher/hostmatcher.go reservedIPNets leftover of CVE-2026-22874. RFC 6890 0.0.0.0/8 not listed. Go IsGlobalUnicast is true for 0.0.0.1.

---

## Entry

- **Method:** `POST`
- **Path:** `/api/v1/repos/{owner}/{repo}/hooks`
- **Router:** Authenticated webhook create + test. hostmatcher reservedIPNets misses 0.0.0.0/8. Delivery stores the HTTP body in hook history.
- **Notes:** Authenticated unpublished Gitea #3 CWE-918 v1.27.3. Witness: GITEA-0000-SSRF in hook history. Not eval. Not a reverse shell. 127.0.0.1 on the same port must stay blocked.

### Call chain

- `POST /api/v1/repos/{owner}/{repo}/hooks url=http://127.0.0.1:8080/ssrf`
- `POST .../hooks/{id}/tests then GET hook history — deny`
- `POST /api/v1/repos/{owner}/{repo}/hooks url=http://0.0.0.1:8080/ssrf`
- `hostmatcher reservedIPNets miss 0.0.0.0/8 — delivery stores body`

### Lab preconditions

- Gitea 1.27.3
- Account that can create a repo webhook
- Oracle sharing Gitea netns on port 8080

### Witness

hook history for 0.0.0.1 contains GITEA-0000-SSRF; 127.0.0.1 webhook denied

### Not success

- eval/base64/system payload
- reverse shell
- X-Gitea-Internal-Auth
- 127.0.0.1 delivery succeeding

---

## Patch / remediation

**Do this first:** Apply the vendor patch for **Gitea**. See references.

**Verify after upgrade**

- Re-run `gitea-hostmatcher-0000-ssrf-Abraxas-Labs.py` against the patched build: the mapped witness must **not** appear.
- Confirm the vendor advisory / changeset in the deployed tree (see references).
- A WAF signature is delay, not a patch.

**If you cannot update immediately**

- Disable or isolate the affected component.
- Hunt for the witness condition on production (new privileged users, unexpected files, injected rows — whatever this CVE's map names).

---

## Reproduction (authorized lab)

Target **only** `http://127.0.0.1:8088` (or the loopback you bound). Do not point this script at the internet.

```bash
python3 gitea-hostmatcher-0000-ssrf-Abraxas-Labs.py
```

Success is the **witness** above in the response body. Generic 200 HTML is not it.

---

## Lab images

Loopback stack used to reproduce. Official images unless a `Dockerfile` in this folder builds from source.

- [`lab/docker-compose.yml`](lab/docker-compose.yml)
- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/run.sh`](lab/run.sh)

```bash
cd lab
docker compose up --force-recreate
```

Bind the vulnerable product tree next to Compose if the YAML mounts a local directory (plugin zip / source tag from the version table). Publish nothing except `127.0.0.1`.

---

## References

- [github.com/go-gitea/gitea](https://github.com/go-gitea/gitea) tag v1.27.3

- Abraxas Labs: [abraxaslabs.tech](https://abraxaslabs.tech) · [github.com/abraxas](https://github.com/abraxas) · [@abraxas_null](https://x.com/abraxas_null)

---

## Records (structured)

```
# Gitea unpublished #3 — hostmatcher 0.0.0.0/8 SSRF

CWE: CWE-918
Severity: High (source review)

## Description

`reservedIPNets` after CVE-2026-22874 still omits RFC 6890 `0.0.0.0/8`. A signed-in user can set a webhook to `http://0.0.0.1` and read the full HTTP body from hook history. `127.0.0.1` on the same port is denied.

## Product

Gitea 1.27.3. Lab oracle is GITEA-0000-SSRF in hook history, not a shell.
```

---

## License

This disclosure pack is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](LICENSE).

---

## Disclaimer

This pack is for **the vendor, the site owner, and licensed labs**. The script talks to `127.0.0.1`. Using it against systems you do not own is not authorized by Abraxas Labs. No warranty.

<p align="center">
  <a href="https://abraxaslabs.tech">abraxaslabs.tech</a> ·
  <a href="https://github.com/abraxas">github.com/abraxas</a> ·
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
</p>
