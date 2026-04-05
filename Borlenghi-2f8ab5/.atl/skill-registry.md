# Skill Registry

**Project**: Borlenghi-2f8ab5
**Generated**: 2026-03-25

## SDD Skills (Orchestrator Phase Skills)

These are loaded by the orchestrator when launching sub-agents for SDD phases. They are NOT loaded by sub-agents directly — the orchestrator passes the resolved path in the launch prompt.

| Name | Description | Path |
|------|-------------|------|
| `sdd-explore` | Explore and investigate ideas before committing to a change | `~/.config/opencode/skills/sdd-explore/SKILL.md` |
| `sdd-propose` | Create a change proposal with intent, scope, and approach | `~/.config/opencode/skills/sdd-propose/SKILL.md` |
| `sdd-spec` | Write specifications with requirements and scenarios (delta specs) | `~/.config/opencode/skills/sdd-spec/SKILL.md` |
| `sdd-design` | Create technical design document with architecture decisions | `~/.config/opencode/skills/sdd-design/SKILL.md` |
| `sdd-tasks` | Break down a change into an implementation task checklist | `~/.config/opencode/skills/sdd-tasks/SKILL.md` |
| `sdd-apply` | Implement tasks from the change, writing actual code | `~/.config/opencode/skills/sdd-apply/SKILL.md` |
| `sdd-verify` | Validate that implementation matches specs, design, and tasks | `~/.config/opencode/skills/sdd-verify/SKILL.md` |
| `sdd-archive` | Sync delta specs to main specs and archive a completed change | `~/.config/opencode/skills/sdd-archive/SKILL.md` |
| `sdd-init` | Initialize Spec-Driven Development context in any project | `~/.config/opencode/skills/sdd-init/SKILL.md` |

## User Skills

Skills installed by the user that are available for sub-agents to load.

| Name | Description | Trigger | Path |
|------|-------------|---------|------|
| `go-testing` | Go testing patterns for Gentleman.Dots, including Bubbletea TUI testing | When writing Go tests, using teatest, or adding test coverage | `~/.config/opencode/skills/go-testing/SKILL.md` |
| `skill-creator` | Creates new AI agent skills following the Agent Skills spec | When user asks to create a new skill, add agent instructions, or document patterns for AI | `~/.config/opencode/skills/skill-creator/SKILL.md` |

## Project Conventions

No project-level convention files detected (no `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, or `copilot-instructions.md` in project root).

## Usage

When the orchestrator launches a sub-agent, it includes a `SKILL: Load \`{path}\` before starting.` instruction if a skill is relevant. The sub-agent loads that file and follows it.

If no skill path was provided, the sub-agent proceeds without loading additional skills — this is not an error.
