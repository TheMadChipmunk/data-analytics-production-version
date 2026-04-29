> ⚙️ **Optional Enrichment:** This challenge adds professional deployment workflow — separating dev and production environments. Complete it if you have time or are interested in how analytics teams manage environments.

## Context

In Challenge 01 you built the complete Greenweez pipeline. Now you'll add the most important professional workflow in analytics engineering: separating your **development environment** (where you experiment safely) from your **production environment** (where tested models serve live dashboards). One flag — `--target prod` — controls which environment dbt writes to.

## Objective

Add a `prod` target to `profiles.yml` alongside the `dev` target from Challenge 01, then deploy your existing Greenweez pipeline to both environments:

```text
~/.dbt/profiles.yml
├── dev  →  dev_database.duckdb  →  main_staging, main_intermediate, main_marts
└── prod →  dev_database.duckdb  →  analytics_prod_staging, analytics_prod_intermediate, analytics_prod_marts
```

Both targets point to the same database file — isolation comes from separate schema namespaces, not separate files.

---

## Section 0: Copy Your Project

> **Working directory convention for this challenge:** `dbt` commands run from **inside** `greenweez_dbt/`. `git` commands run from the **challenge directory** (one level up). Each block below is labelled.

### 0.1 Copy greenweez_dbt from the previous challenge

**📍 In your terminal (challenge directory):**

```bash
# Check the name of your previous challenge directory
ls ..

cp -rP ../../../{{ local_path_to("03-Data-Transformation/10-DBT-Advanced/05-Marketing-Campaign-Data") }}/greenweez_dbt .
```

This copies everything — project files, model definitions, and the `dev_database.duckdb` symlink. The symlink points to the shared database at `03-Data-Transformation/dbt-shared/greenweez.duckdb`. You do not need to re-run `make setup`.

### 0.2 Verify the connection

**📍 In your terminal (into greenweez_dbt/):**

```bash
cd greenweez_dbt
dbt debug
```

You should see `Connection test: OK`. If not, check your `~/.dbt/profiles.yml` path.

**📍 In your terminal (challenge directory — `cd ..` first):**

```bash
git add greenweez_dbt/
git commit -m "Copy Greenweez pipeline from previous challenge"
git push origin master
```

---

## Section 1: Understand Dev vs Production

Before configuring anything, understand what you're building:

**Dev:** experiment and iterate safely — used by default (`dbt run` with no flag), writes to `main_*` schemas, visible only to you.

**Prod:** stable data for live dashboards — requires explicit `--target prod`, writes to `analytics_prod_*` schemas, visible to the whole team.

**The DuckDB approach:** both targets point to the same database file. Isolation comes from different schema namespaces. Raw source tables live in the `raw` schema and are accessible from either target.

---

## Section 2: Configure a Production Target

### 2.1 Edit profiles.yml

**📝 In VS Code**, open `~/.dbt/profiles.yml` (run `code ~/.dbt/profiles.yml`). Your current file has only a `dev` target from the previous challenge. Add a `prod` output:

```yaml
greenweez_dbt:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: dev_database.duckdb
      threads: 4

    prod:
      type: duckdb
      path: dev_database.duckdb
      schema: analytics_prod
      threads: 4
```

**What changed:**

- `path`: both dev and prod point to the same `dev_database.duckdb` file
- `schema`: not set in dev (defaults to `main`) — set to `analytics_prod` in prod

Adding `schema: analytics_prod` to the `prod` target means dbt prefixes all model schemas with `analytics_prod_` — so `staging` becomes `analytics_prod_staging`, `marts` becomes `analytics_prod_marts`, and so on.

### 2.2 Verify the prod target

**📍 In your terminal (inside greenweez_dbt/):**

```bash
dbt debug --target prod
```

You should see `Connection test: OK`.

### Checkpoint 1: Production Environment Configuration

**📍 In your terminal (challenge directory — `cd ..` first):**

```bash
pytest tests/test_production_config.py tests/test_schema_target.py -v
```

**Expected:**

- 1 passed (test_production_config)
- 1 passed (test_schema_target)

The `prod` target is configured in your profile and `dbt debug` confirms it connects. Now you'll actually deploy — run the same pipeline with `--target prod` and verify the models land in the production schemas.

---

## Section 3: Deploy to Production

### 3.1 Build in dev

Confirm the pipeline still runs correctly after copying:

**📍 In your terminal (inside greenweez_dbt/):**

```bash
dbt build
```

All models and tests should pass. Models land in `main_staging`, `main_intermediate`, `main_marts` — same as dev.

### 3.2 Deploy to prod

**📍 In your terminal (inside greenweez_dbt/):**

```bash
dbt build --target prod
```

Watch the schema names in the output — they now show `analytics_prod_` prefixes. The SQL is identical to dev; only the destination changes.

### 3.3 Query both environments in DBeaver

**🗄️ In DBeaver**, connect to `dev_database.duckdb`. Expand the schema list — you should now see both sets of schemas:

- `main_staging`, `main_intermediate`, `main_marts` — dev models
- `analytics_prod_staging`, `analytics_prod_intermediate`, `analytics_prod_marts` — prod models
- `raw` — source tables, accessible from both

Run the same query against both environments:

```sql
SELECT COUNT(*) FROM main_marts.finance_days;
SELECT COUNT(*) FROM analytics_prod_marts.finance_days;
```

Both should return the same row count — same source data, different schema namespace.

### Checkpoint 2: Git Workflow

**📍 In your terminal (challenge directory — `cd ..` first):**

```bash
pytest tests/test_git_workflow.py tests/test_production.py -v
```

**Expected:**

- 2 passed (test_git_workflow)
- 5 passed (test_production)

**To run all tests together:**

```bash
make
```

**Expected:** 9 passed

---

Both environments have been built and verified. The dev/prod separation is now part of your workflow.

## 🎉 Challenge Complete

### Key takeaways

- **Default = dev, explicit = prod** — `dbt build` always uses your `dev` target; `--target prod` must be intentional
- **Same SQL, different destination** — `--target` changes where models land, not what SQL runs
- **Never develop directly in prod** — every change goes through dev first, then gets deployed deliberately
