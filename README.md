# Smart Contract PR Reviewer

This GitHub Action uses a custom LLM backend to review Solidity PRs and automatically comment on detected issues.

## Usage

```yaml
- uses: your-org/smart-contract-pr-reviewer@v1
  with:
    backend_url: https://your-api.domain
```

## Features

- 🎯 PR diff + file change detection
- 🔐 LLM-based security auditing
- 📝 Automatic GitHub comment posting

## Inputs

| Name         | Required | Description                          |
|--------------|----------|--------------------------------------|
| `backend_url`| ✅       | Your hosted review API endpoint      |
