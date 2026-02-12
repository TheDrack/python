# Workflow Fixes Documentation

## Problem Statement (Portuguese)
> o workflow do metabolismo do Jarvis e auto evolution trigger, deram falha, além de não retornar nenhuma informação sobre.
> encontre o motivo dos erros, encontre a solução e execute as.

Translation: "The Jarvis metabolism workflow and auto evolution trigger failed, and did not return any information about it. Find the reason for the errors, find the solution and execute them."

## Issues Identified

### 1. GitHub Copilot CLI Outdated Command
**File:** `scripts/metabolism_mutator.py`

**Problem:** The script was trying to use `gh copilot suggest -t shell` which is an outdated command that no longer exists in the current GitHub Copilot CLI.

**Error Message:**
```
error: unknown option '-t'
Try 'copilot --help' for more information.
```

**Solution:** 
- Removed the outdated `gh copilot suggest` command
- Updated the script to create detailed mutation markers instead
- Added contextual information to guide future implementation
- Prepared for future integration with GitHub Copilot Agent

### 2. Lack of Error Handling and Output Visibility
**Files:** 
- `.github/workflows/jarvis_metabolism_flow.yml`
- `.github/workflows/auto_evolution_trigger.yml`

**Problem:** When scripts failed, the workflows didn't capture or display error messages, making debugging impossible.

**Solution:**
- Added comprehensive error capturing using `set +e`/`set -e` pattern
- All script outputs are now captured and displayed in workflow summaries
- Error codes are checked and reported
- Failed steps show complete error messages and stack traces

### 3. Output Variable Issues
**File:** `scripts/metabolism_analyzer.py`

**Problem:** When `mutation_strategy` was `None`, it was written as the string "None" instead of an empty string, causing issues in workflow conditionals.

**Solution:**
- Changed `result.get('mutation_strategy', '')` to `result.get('mutation_strategy') or ''`
- This ensures `None` values become empty strings instead of "None"

## Changes Made

### 1. `scripts/metabolism_mutator.py`
```python
# OLD (broken):
result = subprocess.run(
    ['gh', 'copilot', 'suggest', '-t', 'shell', prompt],
    ...
)

# NEW (working):
logger.info("🤖 Preparando para consultar GitHub Copilot...")
logger.warning("⚠️ Integração com Copilot Agent em desenvolvimento")
logger.info("📝 Criando marcador para implementação assistida...")
return self._create_manual_marker(intent, impact, issue_body, prompt)
```

### 2. `scripts/metabolism_analyzer.py`
```python
# Fixed output handling
f.write(f"mutation_strategy={result.get('mutation_strategy') or ''}\n")
```

### 3. `.github/workflows/jarvis_metabolism_flow.yml`
```yaml
# Added comprehensive error handling
- name: 🔬 Análise Metabólica - Interpretação da Intenção
  run: |
    set +e  # Don't stop on errors to capture output
    OUTPUT=$(python scripts/metabolism_analyzer.py ... 2>&1)
    EXIT_CODE=$?
    set -e
    
    # Show complete output
    echo "$OUTPUT"
    echo "$OUTPUT" | tail -50 >> $GITHUB_STEP_SUMMARY
    
    # Check for errors
    if [ $EXIT_CODE -ne 0 ] && [ $EXIT_CODE -ne 1 ]; then
      echo "**❌ ERROR (code: $EXIT_CODE)**" >> $GITHUB_STEP_SUMMARY
      exit $EXIT_CODE
    fi
```

### 4. `.github/workflows/auto_evolution_trigger.yml`
```yaml
# Added error handling and better output
- name: 🧬 Verificar se deve triggar evolução
  run: |
    set +e
    python - << 'PYCODE' 2>&1 | tee /tmp/auto_evolution_check.log
    try:
        # ... code ...
    except Exception as e:
        print(f'❌ ERRO: {e}', file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
    PYCODE
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -ne 0 ]; then
      cat /tmp/auto_evolution_check.log >> $GITHUB_STEP_SUMMARY
    fi
```

### 5. `.gitignore`
```
# Added to prevent committing workflow artifacts
.github/metabolism_logs/
.github/metabolism_markers/
```

## Testing

Created comprehensive test suite in `tests/test_workflow_fixes.py` that validates:

1. **Metabolism Analyzer**
   - Produces correct GITHUB_OUTPUT variables
   - Handles `None` values correctly
   - Exit codes work properly

2. **Metabolism Mutator**
   - Executes without errors
   - Creates mutation markers successfully
   - Returns correct success status

3. **Auto Evolution Service**
   - Parses ROADMAP.md correctly
   - Finds next missions
   - Detects auto-evolution PRs properly

**Test Results:** ✅ All 3 tests passed

## Verification

To verify the fixes work correctly:

```bash
# Test metabolism analyzer
export GITHUB_OUTPUT=/tmp/test.txt
python scripts/metabolism_analyzer.py \
  --intent "correção" \
  --instruction "Test fix" \
  --context "Test context with sufficient length"

# Test metabolism mutator  
python scripts/metabolism_mutator.py \
  --strategy "minimal_change" \
  --intent "test" \
  --impact "test"

# Test auto evolution service
python -c "
from app.application.services.auto_evolution import AutoEvolutionService
svc = AutoEvolutionService()
print(svc.find_next_mission())
"

# Run comprehensive test suite
python tests/test_workflow_fixes.py
```

## Impact

### Before
- ❌ Workflows failed silently
- ❌ No error messages visible
- ❌ Copilot CLI command broken
- ❌ Impossible to debug issues

### After
- ✅ Complete error messages in workflow summaries
- ✅ Clear error codes and stack traces
- ✅ Graceful fallback when Copilot not available
- ✅ Easy to debug and understand failures
- ✅ Proper mutation markers created for manual implementation

## Future Improvements

1. **GitHub Copilot Agent Integration**
   - The current implementation creates markers for manual work
   - Future: Integrate with GitHub Copilot Agent API for automatic implementation
   - The markers already include context needed for future automation

2. **Enhanced Error Recovery**
   - Add automatic retry logic for transient failures
   - Implement circuit breakers for external services

3. **Better Monitoring**
   - Add metrics collection for workflow success rates
   - Create alerts for repeated failures

## References

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [GitHub Actions - Handling errors](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepscontinue-on-error)
- Metabolism Flow: `.github/workflows/jarvis_metabolism_flow.yml`
- Auto Evolution: `.github/workflows/auto_evolution_trigger.yml`
