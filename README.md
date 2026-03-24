# GitHub Actions KT — Session 1: Fundamentals

---

## Objective

The goal of this session is to understand GitHub Actions fundamentals, workflow structure, execution flow, and core features used in real-world CI/CD and automation pipelines.

**By the end of this session, you should understand:**
- Workflow structure
- Events and triggers
- Jobs and steps
- Runners
- Inputs and outputs
- Matrix strategy
- Reusable workflows
- Cross-repository workflows
- Logs and debugging
- Job summaries

---

## 1. GitHub Actions in CI/CD (Use Cases)

GitHub Actions is an event-driven automation platform built into GitHub. It allows teams to automate CI/CD pipelines, infrastructure deployments, and repository automation tasks.

### Common Use Cases

| Category        | Example                         |
|-----------------|--------------------------------|
| CI              | Build and test code             |
| Code Quality    | Linting and formatting          |
| Security        | Dependency scanning, SAST       |
| Build           | Package applications            |
| Containers      | Docker build and push           |
| CD              | Application deployment          |
| Infrastructure  | Terraform/CDK deployment        |
| Automation      | PR/Issue automation             |
| Scheduled Jobs  | Cron jobs                       |
| AI              | AI PR review / code analysis    |

**Example Flow:**  
Developer Push → Workflow Trigger → Build → Test → Package → Deploy

---

## 2. Repository Structure (.github vs Other Folders)

GitHub Actions workflows must be placed in a specific directory.

### Standard Repository Structure

```
repo/
  app/
  scripts/
  infra/
  ci/
  .github/
    workflows/
      ci.yml
      deploy.yml
    actions/
      custom-action/
```

### Folder Purpose

| Folder               | Purpose                  |
|----------------------|-------------------------|
| .github/workflows    | Workflow files          |
| .github/actions      | Custom reusable actions |
| ci/                  | Reusable workflows      |
| scripts/             | Shell/Python/Node scripts|
| infra/               | Terraform/CDK           |
| app/                 | Application code        |

> **Important:** Only workflows inside `.github/workflows/` are executed automatically.

---

## 3. Workflow YAML Structure

A workflow is defined using a YAML file.

**Basic Workflow Example:**

```yaml
name: Basic CI

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run command
        run: echo "Hello GitHub Actions"
```

### Workflow Components

| Field      | Description          |
|------------|---------------------|
| name       | Workflow name       |
| on         | Trigger             |
| jobs       | Jobs to run         |
| runs-on    | Runner              |
| steps      | Steps in job        |
| uses       | Use an action       |
| run        | Run command         |
| env        | Environment variables|
| secrets    | Secure variables    |

---

## 4. Events and Triggers

Workflows run based on events.

### Common Events

| Event              | Use Case              |
|--------------------|----------------------|
| push               | Build                |
| pull_request       | PR validation        |
| workflow_dispatch  | Manual run           |
| schedule           | Nightly jobs         |
| workflow_call      | Reusable workflows   |
| repository_dispatch| Cross-repo trigger   |

**Example:**

```yaml
on:
  push:
    branches: [ main ]

  pull_request:

  workflow_dispatch:

  schedule:
    - cron: "0 2 * * *"
```

---

## 5. Jobs and Job Dependencies

A workflow can have multiple jobs.

**Example**

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running tests"

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - run: echo "Building app"
```

**Key Points**
- Jobs run in parallel by default
- Use `needs` to run jobs in sequence
- Jobs run on separate runners

---

## 6. Steps — uses vs run

Each job contains steps.

| Step Type | Purpose         |
|-----------|----------------|
| uses      | Reusable action|
| run       | Shell command  |

**Example:**

```yaml
steps:
  - uses: actions/checkout@v4
  - run: npm install
  - run: npm test
```

---

## 7. Running Scripts (Bash / Python / Node / TypeScript)

Workflows can run scripts written in different languages.

**Bash Example**
```yaml
- run: bash scripts/build.sh
```

**Python Example**
```yaml
- run: python scripts/test.py
```

**Node Example**
```yaml
- run: node scripts/app.js
```

**TypeScript Example**
```yaml
- run: npx ts-node scripts/app.ts
```

---

## 8. Inputs (Manual Inputs / workflow_dispatch)

Manual workflows can accept inputs.

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Environment"
        required: true
        default: "dev"
```

**Use input:**

```yaml
- run: echo "Deploying to ${{ github.event.inputs.environment }}"
```

**Use Cases**
- Manual deployment
- Choose environment
- Choose version
- Run specific job

---

## 9. Passing Data Between Steps and Jobs

**Step Output Example**
```yaml
- name: Set output
  id: step1
  run: echo "version=1.0" >> $GITHUB_OUTPUT

- name: Use output
  run: echo "Version is ${{ steps.step1.outputs.version }}"
```

**Job Output Example**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.step1.outputs.version }}
```

**Artifacts Example**
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: build/
```

---

## 10. Matrix Strategy

Matrix allows running jobs multiple times with different configurations.

```yaml
strategy:
  matrix:
    python-version: [3.10, 3.11]
```

**Use case:**
- Test multiple versions
- Multiple environments
- Parallel jobs

---

## 11. Reusable Workflows

Reusable workflows allow sharing workflow logic across repositories.

**Reusable Workflow**
```yaml
on:
  workflow_call:
```

**Calling Reusable Workflow**
```yaml
jobs:
  call-workflow:
    uses: org/repo/.github/workflows/ci.yml@main
```

---

## 12. Reusable Actions

Custom reusable actions are stored in:

```.github/actions/
```

**Example**
```yaml
- uses: ./.github/actions/docker-build
```

---

## 13. Cross-Repository Workflows

Trigger workflows in another repository.

**Example**
```yaml
- name: Trigger workflow in another repo
  run: |
    curl -X POST \
    -H "Authorization: token ${{ secrets.TOKEN }}" \
    https://api.github.com/repos/org/repo/dispatches \
    -d '{"event_type":"deploy"}'
```

---

## 14. Runners — GitHub-hosted vs Self-hosted

| Runner           | Description           |
|------------------|----------------------|
| GitHub-hosted    | Managed by GitHub    |
| Self-hosted      | Your own server      |

**When to Use Self-hosted**
- Private network access
- Deploy inside VPC
- Large builds
- Custom tools
- Security restrictions

---

## 15. Logs and Debugging

When workflow fails:
1. Open Actions tab
2. Select workflow
3. Select job
4. Select failed step
5. Check logs
6. Fix and rerun

---

## 16. Job Summary and Reporting

You can write summary information:

```yaml
- name: Add summary
  run: |
    echo "## Build Summary" >> $GITHUB_STEP_SUMMARY
    echo "Build completed successfully" >> $GITHUB_STEP_SUMMARY
```

This appears in the workflow summary page.
docs: improve README.md formatting with GitHub Markdown markup