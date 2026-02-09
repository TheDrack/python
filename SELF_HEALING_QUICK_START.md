# Jarvis Self-Healing Quick Reference

## 🚀 Quick Setup (5 minutes)

### 1. Configure API Keys (Required)

Add to GitHub repository **Settings → Secrets and variables → Actions**:

```
GROQ_API_KEY = your_groq_api_key_here
```

Optional (fallback):
```
GOOGLE_API_KEY = your_google_api_key_here
```

**Get API Keys:**
- Groq: https://console.groq.com/
- Google: https://aistudio.google.com/apikey

### 2. Enable Workflows

Workflows are already configured and active! They will trigger automatically.

### 3. Test the System

Create an issue with the label `jarvis-auto-report`:

```
Title: Test Auto-Fix

Body:
Error in app/main.py line 10:
NameError: name 'undefined_var' is not defined
```

Watch Jarvis create a PR automatically! 🎉

---

## 📋 How It Works

### Scenario 1: Manual Issue Report

```
User creates issue → Jarvis detects → Analyzes with AI → Creates PR → Closes issue
```

### Scenario 2: CI Failure (Automatic)

```
CI fails → Issue created → Jarvis triggered → Analyzes → Creates PR → Closes issue
```

---

## 🎯 Usage Examples

### Example 1: Bug Fix

```markdown
Title: Fix authentication error
Label: jarvis-auto-report

Error in app/auth.py line 25:
TypeError: 'NoneType' object is not subscriptable

File "app/auth.py", line 25
  return user['id']
```

**Result:** Jarvis adds null check and creates PR

### Example 2: Documentation Update

```markdown
Title: Add installation guide
Label: jarvis-auto-report

Please add a section about installation to README.md
Include pip install instructions and Python version requirements
```

**Result:** Jarvis generates installation section and creates PR

### Example 3: Feature Request

```markdown
Title: Add user validation
Label: jarvis-auto-report

Please implement user input validation in app/forms.py
Check for empty strings and invalid email formats
```

**Result:** Jarvis implements validation logic and creates PR

---

## 🔍 Monitoring

### Check Workflow Status

1. Go to **Actions** tab
2. Select workflow:
   - "Jarvis Self-Healing Workshop" (for issues)
   - "Auto-Heal CI Failures" (for CI failures)
   - "CI Failure to Issue" (monitors CI)
3. View logs and status

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "Could not extract file" | Include file path in issue body |
| "No API keys found" | Check GROQ_API_KEY secret is set |
| "Failed to create PR" | Check workflow has write permissions |
| Workflow not triggering | Ensure `jarvis-auto-report` label is added |

---

## ⚙️ Advanced Configuration

### Monitor Additional Workflows

Edit `.github/workflows/auto-heal.yml`:

```yaml
on:
  workflow_run:
    workflows: ["Python Tests", "Build", "Deploy"]  # Add your workflows
    types:
      - completed
```

### Change AI Model

Set environment variables in workflow:

```yaml
env:
  GROQ_MODEL: llama-3.3-70b-versatile
  GEMINI_MODEL: gemini-1.5-flash
```

### Disable Auto-Close of Issues

Edit `scripts/auto_fixer_logic.py`, comment out:

```python
# self.close_issue(issue_id)
```

---

## 📊 System Capabilities

✅ **Supported Operations:**
- Fix Python bugs (syntax, runtime, imports)
- Update documentation files
- Modify configuration files
- Implement simple features
- Fix CI/CD failures

❌ **Not Suitable For:**
- Complex architectural changes
- Multi-file refactoring
- Database migrations
- Security vulnerabilities (requires manual review)

---

## 🆘 Getting Help

1. **Review Documentation:** [JARVIS_SELF_HEALING_GUIDE.md](JARVIS_SELF_HEALING_GUIDE.md)
2. **Check Workflow Logs:** Actions → Select workflow → View logs
3. **Create Issue:** Use title "Help with Self-Healing" (without `jarvis-auto-report` label)

---

## 🎓 Best Practices

1. ✅ **Always review** PRs before merging
2. ✅ **Include file paths** in error reports
3. ✅ **Use clear error messages** for better AI analysis
4. ✅ **Test in non-production** branches first
5. ✅ **Monitor API costs** if using paid tiers

---

## 📈 Success Metrics

Track your auto-fix success:
- Number of issues auto-resolved
- Time saved on bug fixes
- PR creation rate
- Merge rate of auto-generated PRs

---

**Questions?** See full documentation: [JARVIS_SELF_HEALING_GUIDE.md](JARVIS_SELF_HEALING_GUIDE.md)
