# Contributing to simple-api-server

Thank you for considering contributing to **simple-api-server**! 🎉  
We appreciate your support in improving this project.

---

## Code of Conduct

Please review and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) to help us maintain a welcoming and respectful community.

---

## How to Contribute

### Reporting Bugs

When reporting a bug, please include:
- A clear and descriptive title.
- Steps to reproduce the issue.
- Expected vs actual behavior.
- Screenshots or logs, if available.
- Environment details (OS, API version, etc.).

Before reporting a bug, please search existing issues to avoid duplicates.

---

### Requesting Features

We welcome feature suggestions!  
When creating a feature request, please include:
- A description of the proposed feature.
- Why it would benefit the project.
- Any relevant use cases or examples.

---

### Submitting Changes (Pull Requests)

1. **Fork** this repository.
2. **Clone** your fork:
    ```bash
    git clone https://github.com/your-username/simple-api-server.git
    ```
3. **Create a feature branch**:
    ```bash
    git checkout -b feature/your-branch-name
    ```
4. **Make your changes** following the [Coding Standards](#coding-standards).
5. **Test your changes** locally to ensure they don't break existing functionality.
6. **Commit your changes** using the [Commit Message Guidelines](#commit-message-guidelines) below.
7. **Push to your fork**:
    ```bash
    git push origin feature/your-branch-name
    ```
8. **Submit a Pull Request** targeting the `main` branch.

Your Pull Request must:
- Be focused on a single feature or fix.
- Pass all tests and CI checks.
- Include updated documentation if the feature or behavior changes.
- Reference related issue numbers if applicable.

---

## Coding Standards

- **Language**: [Specify if Node.js, Python, Java, etc.]
- Use 2 spaces for indentation.
- Follow REST API best practices for API-related changes.
- Write clear, modular, and well-documented code.
- Add or update unit/integration tests for any new or changed functionality.

---

## Commit Message Guidelines

We use **JIRA-style commit messages** to link changes directly to task tracking.

### Format:

**Example Commit Messages**:
- `SAPI-102: Fix authentication error for login endpoint`
- `SAPI-215: Add health check endpoint`
- `SAPI-301: Refactor user service for better scalability`

Where:
- `PROJECTKEY` is the key for the JIRA project (e.g., `SAPI` for "Simple API Server").
- `1234` is the JIRA issue number.

> If you are unsure which ticket to reference, please ask a maintainer before submitting your PR.

---

## Running Tests

Before submitting your Pull Request:
- Run all unit and integration tests.
- Ensure your changes do not introduce new errors or break the build.

```bash
pytest
```
