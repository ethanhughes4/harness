# Harness

**An AI-powered software development harness for Claude Code.**

Harness turns an application idea into a structured software development process. It coordinates planning skills, builder agents, automated tests, specialised reviewers and controlled integration to help build applications in manageable, verifiable stages.

Instead of asking an AI to build an entire application in one long conversation, Harness breaks the work into features, checks the results, reviews completed work in batches, and keeps track of progress throughout development.

Its goal is to make AI-assisted software development more organised, reliable and cost-efficient.

## What Does Harness Do?

- **Requirements discovery:** Uses a questions skill to understand what the user wants to build.
- **Requirements validation:** Checks the answers for missing information, contradictions and unclear requirements before development begins.
- **Project planning:** Converts the agreed requirements into a technical plan, architecture and structured feature list.
- **Feature development:** Uses builder agents and relevant skills to implement features in a controlled order.
- **Automated testing:** Runs configured tests and checks on individual features throughout development.
- **Batch code reviews:** Reviews multiple completed features in a single reviewer invocation while retaining separate verdicts for each feature.
- **Security reviews:** Applies additional scrutiny to high-risk features, such as authentication, payments and sensitive database changes.
- **UI/UX reviews:** Evaluates usability and visual quality at defined milestones and at the end of the build.
- **Targeted rework:** Sends only the features that need changes back through implementation and verification.
- **Controlled integration:** Merges eligible low-risk features after successful checks while keeping high-risk changes under human control.
- **Progress tracking:** Records completed work, review results, decisions and outstanding issues so development can continue across sessions.

## How Harness Works

Harness follows a structured workflow from the initial idea to the final application. The orchestrator coordinates the stages, invokes the relevant skills and agents, and determines what should happen next based on the results.

### 1. Project Discovery — Questions Skill

The process begins by asking the user questions about the application they want to build.

These questions establish the purpose of the application, target users, required functionality, constraints, preferences and expected outcomes.

The objective is to understand the problem before deciding how to solve it.

### 2. Requirements Validation — Review Skill

Once the answers have been collected, the requirements are checked for completeness and consistency.

This stage looks for missing information, contradictory answers, unclear requirements and potential technical concerns.

If clarification is needed, the workflow returns to the user before proceeding. This helps prevent incorrect assumptions from spreading into the design and implementation.

### 3. Planning and Design — Planning and UI/UX Skills

The validated requirements are converted into an implementation plan.

This includes the technical approach, architecture, development decisions, feature breakdown and dependencies.

For applications with a user interface, the relevant design skills establish the visual direction and guide the interface design.

The result is an agreed plan that can be translated into individual features.

### 4. Feature Preparation — Test-Writing Skill

Before implementation, the planned features are prepared with acceptance criteria and appropriate tests.

Dependencies are identified so features are built in a sensible order.

The project is also configured with the instructions and testing commands required by the build process.

This establishes how the completed work will be verified against the agreed requirements.

### 5. Feature Development — Builder Agent

The builder agent implements features using the relevant programming, framework, design and other applicable skills.

Features are developed in separate branches to isolate changes and control integration.

Harness selects features whose dependencies are satisfied and respects the configured limit on concurrent builders.

Each feature is developed against its own requirements rather than relying on the AI to remember the entire application throughout one long conversation.

### 6. Automated Verification — Tests and Gates

Every feature runs through its required automated checks before proceeding to review.

Depending on the project, these can include acceptance tests, unit tests, linting, type checking, builds and other configured validations.

The workflow also classifies the feature's risk so that additional controls can be applied when necessary.

A failed gate must be addressed before the feature can proceed as though it passed.

### 7. Batch Reviews — Independent Reviewer Agents

Once the selected features have completed their required checks, Harness coordinates the applicable reviews.

Rather than launching a separate code-review invocation for every feature, compatible features are reviewed together.

The review stage can include:

- **Code reviewer:** Reviews the batch for correctness, implementation quality, compliance with requirements and other relevant problems.
- **Security reviewer:** Reviews high-risk features for security vulnerabilities and unsafe implementation decisions.
- **User-experience reviewer:** Evaluates usability and the experience of using the application at configured milestones.
- **Visual reviewer:** Evaluates the application's visual design at configured milestones.

Not every reviewer runs for every feature. Code review applies to eligible batches, security review is triggered for high-risk work, and UI/UX reviews run at the configured milestones and at the end of the build.

Each reviewer performs its designated checks and returns findings for the orchestrator to process.

### 8. Review Results — The Orchestrator Decides What Happens Next

The orchestrator collects the review results and determines the next action for each feature independently.

**Pass**

The feature can proceed towards integration once all required checks and reviews have passed.

**Changes required**

The feature returns to the builder for targeted corrections. The relevant checks and reviews are repeated after the changes.

**Human approval required**

High-risk changes are held for human inspection and approval rather than being merged automatically.

A successful review of one feature does not automatically mean another feature in the same batch has passed.

### 9. Targeted Rework — Fix Only What Failed

When a feature fails a test or review, Harness records the problem and sends the affected work back for correction.

The builder addresses the findings, the required automated checks run again, and the relevant reviews are repeated.

Features that have already passed are not unnecessarily rebuilt or re-reviewed simply because another feature failed.

This keeps the workflow focused on the outstanding problems and avoids repeating completed work without a reason.

### 10. Controlled Integration — Merge and Verify

Once a feature satisfies its requirements, gates and applicable review rules, it can proceed to integration.

Eligible low-risk features are merged through the controlled merge process, followed by the configured project tests.

High-risk features remain on their branches until the user approves them through the dedicated approval workflow.

If integration tests fail, the workflow must address the failure rather than treating the merge as a successful completion.

### 11. Final Verification and Reporting

After the planned features have been completed, Harness performs the final applicable checks.

For applications with a user interface, the final walkthrough evaluates the integrated application rather than only looking at individual features.

The project records are then used to report what has been completed, which checks passed, what remains outstanding and which items require human attention.

The result is a development process that can be inspected and resumed, rather than a single AI conversation with no clear record of its progress.

## Batch Processing and Token Efficiency

A key design goal of Harness is to reduce unnecessary AI calls while maintaining meaningful verification and independent review.

Repeatedly starting a new reviewer for every feature can duplicate context and increase token consumption. Harness addresses this by grouping compatible features into review batches.

### How Batching Works

1. **Select features:** Choose features whose dependencies are satisfied, within the configured concurrency limit.
2. **Build the selected features:** Use the builder agents and relevant skills to implement the work.
3. **Run individual checks:** Each feature still completes its own required tests, gates and risk classification.
4. **Review the batch:** Once the selected features are ready, invoke the code reviewer for the batch rather than starting a separate code reviewer for each feature.
5. **Keep results separate:** Each feature receives its own review report and verdict. One feature can pass while another requires changes.
6. **Rework selectively:** Only features with outstanding findings return for corrections, additional checks and the necessary repeat reviews.

### Why This Matters

Batching allows the reviewer to reuse shared project context where practical and reduces the number of separate AI invocations.

Additional efficiency measures include:

- Loading relevant skills when needed instead of repeating all instructions at every stage.
- Running specialised reviews only when their configured conditions apply.
- Avoiding unnecessary repetition of reviews for features that have already passed.
- Keeping review findings focused on the affected feature and its relevant code.
- Persisting project state so the workflow can continue without unnecessarily repeating completed stages.

**Batching does not mean skipping tests or combining all features into one shared verdict.** Every feature must still satisfy its own requirements, pass its required checks, and follow the applicable review and integration rules.

The actual token and cost savings depend on the project, the amount of shared context, the number of features, reviewer complexity and how much rework is needed.

## Getting Started

Harness runs as a plugin for [Claude Code](https://code.claude.com/).

### Prerequisites

- Claude Code installed and working.
- Python 3.10 or later.
- Git installed.
- A project directory for the application you want to build.

Browser-based UI testing may also require Playwright and Chromium, depending on the project's configuration.

### 1. Start Claude Code with Harness

Load the Harness plugin using its installation path:

```bash
claude --plugin-dir "/path/to/harness"

## License

See the repository's license file for licensing information.
