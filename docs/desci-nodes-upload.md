# Publishing to DeSci Nodes via API

> Documented from the upload of the SU(2) 3nj paper on 2026-02-27.  
> Node: [dPID 1028](https://dpid.org/1028) — <https://nodes.desci.com/node/NXpP8LNtumD5l3ppX1HcKwcPJ-Hbqc9gHY7TRXQznEk>

---

## Overview

DeSci Nodes is a decentralized open-science platform that creates persistent, versioned research objects (Nodes) with IPFS-backed storage, Ceramic stream history, and minted dPIDs (decentralized persistent identifiers). Publishing is done in three stages:

1. **Create** a private draft Node via the backend REST API  
2. **Upload** files to the Node drive  
3. **Publish** to Ceramic + the dPID alias registry using the `@desci-labs/nodes-lib` JS library  

---

## Prerequisites

| Requirement | Notes |
|---|---|
| DeSci Nodes account | <https://nodes.desci.com> |
| API key | Generated at <https://nodes.desci.com> → Profile → API Keys |
| Node.js ≥ 18 | ESM support required |
| `@desci-labs/nodes-lib` | `npm install @desci-labs/nodes-lib` |
| An Ethereum private key | Used to sign the Ceramic stream; an ephemeral key generated at publish time is fine — it need not hold funds or be reused |

The API key is stored as `DESCI_NODES_API_KEY` in `.env` (git-ignored). The Ethereum key is ephemeral and never stored.

---

## API Base URL

```
https://nodes-api.desci.com
```

The public-facing website (`nodes.desci.com`) is a Next.js frontend — all API calls go to the `nodes-api` subdomain.

**Authentication**: pass the API key in the `api-key` header (not `Authorization: Bearer`):

```bash
curl -H "api-key: $DESCI_NODES_API_KEY" https://nodes-api.desci.com/v1/nodes
```

---

## Step 1 — Create a draft Node

```bash
APIKEY="<your-api-key>"

curl -s -X POST \
  -H "api-key: $APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Your Paper Title",
    "researchFields": ["Mathematics", "Pure Mathematics"],
    "defaultLicense": "CC-BY-4.0"
  }' \
  https://nodes-api.desci.com/v1/nodes/createDraft
```

The response contains `node.uuid` — save this, it identifies the node for all subsequent operations.

To find valid `researchFields` values:

```bash
curl -s -H "api-key: $APIKEY" \
  "https://nodes-api.desci.com/v1/researchFields?q=math"
```

---

## Step 2 — Upload files

Files are uploaded to the node drive via multipart POST. The `componentType` field sets how the UI categorises the file; use `pdf` for manuscripts and `code` for code/data archives.

```bash
NODE_UUID="<uuid-from-step-1>"

# Upload manuscript PDF
curl -s -X POST \
  -H "api-key: $APIKEY" \
  -F "uuid=${NODE_UUID}" \
  -F "contextPath=root" \
  -F "componentType=pdf" \
  -F "autoStar=true" \
  -F "files=@paper.pdf;type=application/pdf" \
  https://nodes-api.desci.com/v1/data/update

# Upload supplementary zip
curl -s -X POST \
  -H "api-key: $APIKEY" \
  -F "uuid=${NODE_UUID}" \
  -F "contextPath=root" \
  -F "componentType=code" \
  -F "autoStar=true" \
  -F "files=@supplementary.zip;type=application/zip" \
  https://nodes-api.desci.com/v1/data/update
```

Successful responses include a `manifest` block listing all components in the node drive. You can upload multiple files in a single call by repeating `-F "files=@..."`.

---

## Step 3 — Publish (Ceramic + dPID registry)

Publishing requires a local Ethereum signer to create a Ceramic stream and commit the manifest CID. The `@desci-labs/nodes-lib` library handles all of this.

### Setup

```bash
mkdir publish-script && cd publish-script
npm init -y
npm install @desci-labs/nodes-lib viem
```

### publish.mjs

```js
import {
  NODESLIB_CONFIGS,
  setNodesLibConfig,
  setApiKey,
  publishNode,
  signerFromPkey,
} from "@desci-labs/nodes-lib/browser";
import { ethers } from "ethers";

const API_KEY   = process.env.DESCI_NODES_API_KEY;
const NODE_UUID = process.env.NODE_UUID; // from Step 1

setNodesLibConfig(NODESLIB_CONFIGS.prod);
setApiKey(API_KEY);

// Generate a fresh ephemeral signing key — no funds needed
const wallet = ethers.Wallet.createRandom();
console.log(`Ephemeral signer: ${wallet.address}`);
const signer = signerFromPkey(wallet.privateKey);

const result = await publishNode(NODE_UUID, signer, /* mintDoi= */ false);

console.log("dPID:    ", result.dpid);
console.log("Stream:  ", result.ceramicIDs.streamID);
console.log("CID:     ", result.updatedManifestCid);
console.log("URL:     ", `https://nodes.desci.com/node/${NODE_UUID}`);
console.log("dPID URL:", `https://dpid.org/${result.dpid}`);
```

```bash
DESCI_NODES_API_KEY="..." NODE_UUID="..." node publish.mjs
```

**Note:** The `browser` export is used even in Node.js to avoid a transitive `apache-arrow` / FlightSQL dependency that is only needed for Codex query features.

---

## What `publishNode` does internally

1. Calls `prePublishDraftNode` — the backend re-DAGifies the drive and returns an updated manifest CID plus the existing Ceramic stream ID (if any).  
2. Calls `codexPublish` — publishes to Ceramic (ComposeDB), producing a `streamID` + `commitID`.  
3. POSTs to `/v1/nodes/publish` with `{ uuid, cid, manifest, ceramicStream, commitID, useNewPublish: true }` — the backend registers a dPID alias in the on-chain alias registry (Optimism Sepolia) and makes files publicly accessible on IPFS.

---

## Listing and verifying your nodes

```bash
# List all nodes for your account
curl -s -H "api-key: $APIKEY" https://nodes-api.desci.com/v1/nodes

# Check published status
curl -s https://nodes-api.desci.com/v1/nodes/published/<UUID>
```

---

## Results for the SU(2) 3nj paper

| Field | Value |
|---|---|
| Node UUID | `NXpP8LNtumD5l3ppX1HcKwcPJ-Hbqc9gHY7TRXQznEk` |
| dPID | 1028 |
| Node URL | <https://nodes.desci.com/node/NXpP8LNtumD5l3ppX1HcKwcPJ-Hbqc9gHY7TRXQznEk> |
| dPID URL | <https://dpid.org/1028> |
| Manifest CID | `bafkreibcno57wexxw22cxfdt2o4gtww646xoq35upewryov34g6xryzk34` |
| Ceramic stream | `kjzl6kcym7w8y521wa7m34on9hzr9n1ncrymsicmd2v0rj3ibz65x6wiko4jany` |
| License | CC-BY-4.0 |
| Research fields | Mathematics, Pure Mathematics |

Files uploaded:
- `su2-3nj-unified-representations.pdf` — RevTeX/JMP manuscript
- `manuscript_supplementary.zip` — 5 data files (JSON/CSV) + 7 scripts (Wolfram, Python, shell)
