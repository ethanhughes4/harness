# Harness

**An AI-powered software development harness for Claude Code.**

Harness helps you turn an idea into a working software application by automating the planning, building, testing, and review process.

Instead of asking Claude to build an entire application in one go, Harness breaks the work into manageable features, builds them systematically, checks the results, and tracks progress along the way.

## What Does Harness Do?

Harness coordinates the software development process from the initial idea through to a completed application.

- **Project planning:** Turns your idea into requirements, technical decisions, and a structured feature list.
- **Feature development:** Breaks the application into smaller features and builds them in a controlled order.
- **Automated testing:** Runs the configured tests and checks as features are developed.
- **Code review:** Reviews implementations against requirements and identifies problems that need fixing.
- **Security checks:** Applies additional scrutiny to high-risk features such as authentication, payments, and database changes.
- **UI and UX reviews:** Checks the application's user experience and visual design at milestones.
- **Automatic rework:** Sends features back for corrections when tests or reviews identify problems.
- **Progress tracking:** Records completed features, outstanding work, decisions, and review results.
- **Controlled merging:** Integrates approved, low-risk features while keeping high-risk changes available for human approval.

## How It Works

Harness follows a structured development workflow.

1. **Define the project** — Describe what you want to build and clarify the requirements.
2. **Plan the application** — Establish the architecture, design direction, development stages, and feature list.
3. **Prepare the project** — Set up the required project files, instructions, and testing configuration.
4. **Build the features** — Claude develops features in separate branches, respecting dependencies and the configured concurrency limit.
5. **Run automated checks** — Each feature is tested before moving forward.
6. **Review the code** — The code reviewer examines completed work. High-risk features receive additional security review.
7. **Fix any problems** — Features that fail checks or reviews are sent back for targeted corrections.
8. **Review the application** — UI projects receive user-experience and visual reviews at configured milestones and at the end.
9. **Integrate completed work** — Features that pass the required checks are merged according to the project's risk and approval rules.
10. **Track the results** — Progress and outstanding issues remain recorded so development can continue across sessions.

## Batch Processing and Token Efficiency

Harness is designed to reduce unnecessary AI usage while maintaining a structured development and review process.

Rather than launching a separate AI reviewer for every feature, Harness groups compatible work together and reuses review context where possible.

### How Batching Works

1. **Build multiple features:** Harness selects features whose dependencies are satisfied and processes them within the configured concurrency limit.
2. **Check each feature individually:** Every feature still runs its own acceptance tests, automated checks, and risk classification.
3. **Review the batch together:** Once the selected features have passed their required checks, the code reviewer reviews the group in a single invocation rather than starting a separate reviewer for every feature.
4. **Keep results independent:** Each feature receives its own review report and verdict. One feature can pass while another requires changes.
5. **Fix only what needs fixing:** Features that fail review are sent back for targeted rework. Features that have already passed do not need to be reviewed again simply because another feature failed.

### Additional Review Optimisation

Harness also avoids running expensive specialised reviews unnecessarily:

- **Security reviews:** Reserved for high-risk features, such as authentication, payments, secrets, and sensitive database changes.
- **User-experience and visual reviews:** Run at configured milestones and at the end of the build, rather than automatically launching both AI reviewers for every UI feature.
- **Automated checks:** Continue to run on individual features, ensuring that batching reviews does not mean skipping tests.

### Why This Matters

Every unnecessary AI invocation can introduce additional token usage and cost. By batching code reviews, reusing shared context, and running specialised reviews only when appropriate, Harness aims to make larger development projects more efficient.

Batching does not eliminate the need for independent feature verdicts, targeted fixes, or final application checks. It reduces duplicated review effort while preserving the safeguards that make the development process reliable.

Actual savings depend on the size and complexity of the application, the amount of shared context, and how many features require rework.

## Getting Started

Harness runs as a plugin for [Claude Code](https://code.claude.com/).

### Prerequisites

- Claude Code
- Python 3.10 or later
- Git
- A project directory for the application you want to build

Browser-based UI testing may also require Playwright and Chromium, depending on the project configuration.

### 1. Start Claude Code with Harness

Open the project you want to work on and load the Harness plugin:

```bash
claude --plugin-dir "/path/to/harness"
```

Replace `/path/to/harness` with the actual location of your Harness installation.

### 2. Start a Project

Describe the application you want to create:

```text
/harness:new "Describe your application idea here"
```

Follow the prompts to establish the requirements, review the proposed plan, and prepare the project for development.

### 3. Build the Application

Once initialisation is complete, run the build script from the project directory:

```bash
build.cmd
```

Harness works through the planned features, runs the configured checks, and records progress.

The build can be resumed in a later session using the same project state.

## Useful Commands

| Command | Purpose |
| --- | --- |
| `/harness:new` | Start a project or plan additional features. |
| `/harness:report` | Review development progress and outstanding issues. |
| `/harness:rework <id> <note>` | Request changes to a feature. |
| `/harness:approve <id>` | Review and approve a high-risk feature held for human approval. |
| `/harness:smoke` | Run an end-to-end smoke test of the Harness workflow. |

The main build process is started using `build.cmd`.

## Safety and Human Oversight

Harness automates much of the repetitive development work while retaining safeguards around important decisions.

- Low-risk features can be merged automatically after passing their required checks and reviews.
- High-risk features are held for human approval and are not automatically merged.
- Acceptance tests and configured automated checks remain part of the development process.
- Failed reviews trigger targeted corrections rather than requiring the entire project to be rebuilt.
- Changes are developed on separate branches to help isolate work and control integration.

Harness does not guarantee that generated software is bug-free or secure. The finished application should still be reviewed and tested before production use.

## Design Principles

Harness is built around a few core principles:

- **Small, manageable changes:** Build applications feature by feature.
- **Test continuously:** Identify problems before they spread through the application.
- **Use specialised agents:** Give planning, development, and review distinct responsibilities.
- **Minimise unnecessary work:** Batch compatible reviews and avoid repeating expensive checks without a reason.
- **Preserve project state:** Record progress so work can continue across sessions.
- **Keep humans in control:** Escalate high-risk changes rather than merging them automatically.

## Limitations

Harness relies on Claude Code, the quality of the project requirements, and the checks configured for each application.

AI agents may still make mistakes, tests may not cover every scenario, and browser-based reviews can incur additional usage costs. Token consumption varies according to project size, feature complexity, review requirements, and the amount of rework needed.

Harness assists with building and reviewing software; deployment, production configuration, and final release decisions remain separate responsibilities.

## License

See the repository's license file for licensing information.
