---
name: creating
description: Create a new skill with proper structure, reference files, and best practices. Scaffolds SKILL.md, command wrapper, and reference directory.
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Bash(ls *)
  - Bash(mkdir *)
---

# Create a New Skill

Scaffold a well-structured skill following skillforge best practices.

## Workflow

### 1. Gather Requirements

Ask via AskUserQuestion:

```text
Plugin name: [existing plugin or new]
Skill name: [verb-noun format, e.g., generating-dockerfile]
```

Then ask skill type:

```text
What kind of skill is this?

○ Generator (creates files from detection + templates)
○ Auditor (evaluates existing files against checklist)
○ Optimizer (improves existing files)
○ Orchestrator (delegates to other skills)
```

### 2. Determine if References Are Needed

Ask via AskUserQuestion:

```text
Does this skill have variant content based on detection or user choice?

○ Yes, varies by language/ecosystem (e.g., Python vs Node.js)
○ Yes, varies by user choice (e.g., Helm vs kubectl)
○ Yes, catalog of selectable items (e.g., services)
○ No, single workflow for all cases
```

If yes, ask for the variant names (languages, choices, or catalog items).

### 3. Verify Plugin Location

```text
Glob: plugins/{plugin}/skills/
```

If plugin doesn't exist, create the directory structure:

```bash
mkdir -p plugins/{plugin}/{.claude-plugin,commands,skills/{skill-name}/references}
```

If plugin exists but skill doesn't:

```bash
mkdir -p plugins/{plugin}/skills/{skill-name}/references
```

### 4. Generate SKILL.md

Read the appropriate template from `references/` based on skill type:

| Skill Type | Template |
|------------|----------|
| Generator | `references/template-generator.md` |
| Auditor | `references/template-auditor.md` |
| Orchestrator | `references/template-orchestrator.md` |

Apply the template with gathered requirements.

### 5. Generate Reference Files

If variant content was requested, create stub reference files:

```text
references/{variant}.md
```

Each stub follows the reference file anatomy:

```markdown
# {Variant Name}

## Detection

{How to identify when this reference applies}

## Content

{Templates, definitions, or checks specific to this variant}

## Required Variables

{Any configuration the parent skill must provide}
```

### 6. Generate Command Wrapper

Create `commands/{command-name}.md`:

```yaml
---
name: {plugin}:{command-name}
description: {short description}
argument-hint: "{hint}"
---

Invoke the `{plugin}:{skill-name}` skill and follow it exactly.
```

Use the command naming convention:

- `generating-dockerfile` skill → `dockerfile` command
- `generating-deploy` skill → `deploy` command
- `auditing` skill → `audit` command
- `setting-up` skill → `setup` command

### 7. Report

```text
============================================================================
Skill Created: {plugin}:{skill-name}
============================================================================

Files created:
  ✓ skills/{skill-name}/SKILL.md
  ✓ commands/{command-name}.md
  {✓ skills/{skill-name}/references/{variant}.md  (per variant)}

Structure:
  {plugin}/
  ├── commands/{command-name}.md
  └── skills/{skill-name}/
      ├── SKILL.md ({lines} lines)
      └── references/
          {├── {variant}.md  (per variant)}

Next steps:
  1. Fill in reference file content for each variant
  2. Test: claude --plugin-dir ./plugins/{plugin}
  3. Run /skillforge:audit to verify structure
============================================================================
```

## Template Reference Files

- `references/template-generator.md` - Template for generator skills
- `references/template-auditor.md` - Template for auditor skills
- `references/template-orchestrator.md` - Template for orchestrator skills
