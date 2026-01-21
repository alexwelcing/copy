# Agency Command

Launch the marketing agency orchestration system.

## Usage

```
/agency [command] [options]
```

## Commands

### `start`
Initialize the agency with the Mayor agent coordinating work.

### `brief <project-name>`
Create a new creative brief for a marketing project.

### `assign <skill> <agent>`
Assign a specific marketing skill to an agent.

### `status`
Check the status of all active projects and agents.

### `review`
Initiate a creative review workflow.

## Examples

```
/agency start
/agency brief "Product Launch Campaign"
/agency assign copywriting polecat-1
/agency status
```

## Workflow

1. Start the agency to initialize the Mayor
2. Create a brief for your project
3. Mayor analyzes requirements and spawns specialized agents
4. Agents work on assigned skills (copywriting, CRO, SEO, etc.)
5. Work is tracked through convoys and reviewed
6. Final deliverables are compiled and presented
