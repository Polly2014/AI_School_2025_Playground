# Contributing to Multimodal AI Assistant

Thank you for your interest in contributing to the Multimodal AI Assistant project! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment using our setup scripts
4. Create a new branch for your feature or bugfix

## Development Setup

### Windows
```powershell
.\setup.ps1
```

### Linux/Mac
```bash
./setup.sh
```

## Making Changes

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Configure your environment**:
   - Copy `.env.example` to `.env`
   - Add your Azure OpenAI API credentials

3. **Make your changes** and test them locally

4. **Run tests** (if available):
   ```bash
   python -m pytest
   ```

5. **Check code style**:
   ```bash
   pip install black flake8
   black .
   flake8 .
   ```

## Submitting Changes

1. **Commit your changes** with a descriptive message:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub

## Pull Request Guidelines

- **Title**: Use a clear, descriptive title
- **Description**: Explain what changes you made and why
- **Testing**: Describe how you tested your changes
- **Documentation**: Update documentation if needed

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

## Reporting Issues

When reporting issues, please include:

- **Environment**: OS, Python version, dependencies
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Logs**: Any relevant error messages or logs

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists or is planned
2. Open an issue with the "feature request" label
3. Describe the feature and its use case
4. Explain why it would be valuable to users

## Code of Conduct

Please be respectful and inclusive in all interactions. We aim to create a welcoming environment for all contributors.

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Contact the maintainers
- Check the documentation in `CONFIG.md` and `DEPLOYMENT.md`

Thank you for contributing! 🚀
