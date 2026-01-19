# Testing Checklist for Dual CLI Support

Use this checklist to verify both CLIs work correctly with the RLM setup.

## Prerequisites

- [ ] Python 3 installed
- [ ] Claude CLI installed (for testing Claude path) OR
- [ ] GitHub Copilot CLI installed (for testing Copilot path)
- [ ] Large test file available (>500KB recommended)

## Test Files

Create test context file:
```bash
mkdir -p context
# Generate a large test file
python3 -c "for i in range(10000): print(f'Line {i}: This is test content with various topics like security, performance, and architecture.')" > context/test_large.txt
```

## Claude CLI Tests

### Test 1: Basic RLM Skill
```bash
cd claude_code_RLM
claude

# In Claude CLI:
/rlm context=context/test_large.txt query="Find all mentions of security"
```

**Expected:**
- [ ] REPL initializes successfully
- [ ] Context loaded (size displayed)
- [ ] Chunks created (count displayed)
- [ ] rlm-subcall agent invoked for each chunk
- [ ] JSON responses collected
- [ ] Final synthesis provided

### Test 2: Agent Auto-Discovery
```bash
# In Claude CLI:
"Use the rlm-subcall agent to analyze this chunk: [paste small chunk]"
```

**Expected:**
- [ ] Agent found automatically from `.claude/agents/`
- [ ] JSON response returned

## GitHub Copilot CLI Tests

### Test 1: Automatic Orchestration
```bash
cd claude_code_RLM
copilot

# In Copilot CLI:
"Process context/test_large.txt using RLM pattern and find all mentions of security"
```

**Expected:**
- [ ] Copilot reads AGENTS.md
- [ ] REPL initialized
- [ ] Chunks created
- [ ] Multiple task() calls launched (check logs for parallel execution)
- [ ] Results synthesized

### Test 2: Helper Script
```bash
# Initialize REPL
python3 .claude/skills/rlm/scripts/rlm_repl.py init context/test_large.txt

# Create chunks
python3 .claude/skills/rlm/scripts/rlm_repl.py exec -c "paths = write_chunks('.claude/rlm_state/chunks', size=200000); print('\n'.join(paths))"

# Load agent template
python3 scripts/rlm_copilot_helper.py load-agent rlm-subcall

# Prepare chunks
python3 scripts/rlm_copilot_helper.py prepare-chunks "find security" .claude/rlm_state/chunks
```

**Expected:**
- [ ] Agent template prints successfully
- [ ] JSON array with chunk invocations returned
- [ ] Each invocation has: chunk_id, chunk_path, query, agent_template

### Test 3: Manual task() Invocation in Copilot
```bash
# In Copilot CLI after preparing chunks:
"Using the chunk invocations from the helper script, analyze all 5 chunks in parallel using task() calls"
```

**Expected:**
- [ ] Copilot launches 5 task() calls
- [ ] Each uses model="claude-haiku-4.5"
- [ ] All return JSON with required schema
- [ ] Results synthesized

## Verification Tests

### Test 4: Identical Outputs
Run the same query through both CLIs:

**Query:** "Find all mentions of 'performance' and 'architecture'"

**Claude CLI:**
```bash
/rlm context=context/test_large.txt query="Find all mentions of 'performance' and 'architecture'"
```

**Copilot CLI:**
```bash
"Process context/test_large.txt using RLM and find all mentions of 'performance' and 'architecture'"
```

**Compare:**
- [ ] Similar findings identified
- [ ] Confidence levels reasonable
- [ ] Evidence quoted correctly
- [ ] JSON schema consistent

### Test 5: Error Handling
```bash
# Test with missing file
python3 .claude/skills/rlm/scripts/rlm_repl.py init nonexistent.txt
```

**Expected:**
- [ ] Clear error message
- [ ] No crash

```bash
# Test with invalid chunk directory
python3 scripts/rlm_copilot_helper.py prepare-chunks "test" /invalid/path
```

**Expected:**
- [ ] FileNotFoundError with clear message
- [ ] No crash

## Documentation Tests

### Test 6: README Accuracy
- [ ] Installation instructions work
- [ ] Usage examples executable
- [ ] Architecture table accurate
- [ ] File structure matches reality

### Test 7: COPILOT_CLI_GUIDE Accuracy
- [ ] Quick start commands work
- [ ] Example session matches actual behavior
- [ ] Troubleshooting tips resolve issues

## Performance Tests

### Test 8: Parallel Processing (Copilot Only)
```bash
# Create many chunks (20+)
python3 .claude/skills/rlm/scripts/rlm_repl.py exec -c "paths = write_chunks('.claude/rlm_state/chunks', size=50000); print(len(paths))"

# Time the processing
time copilot
# Then: "Process all chunks using RLM pattern"
```

**Expected:**
- [ ] All task() calls launched simultaneously
- [ ] Processing faster than sequential
- [ ] No race conditions or corrupted results

## Cleanup

```bash
# Remove test artifacts
rm -rf .claude/rlm_state/chunks/*
rm .claude/rlm_state/state.pkl
rm context/test_large.txt
```

## Results Summary

| Test | Claude CLI | Copilot CLI | Notes |
|------|-----------|-------------|-------|
| Basic RLM | ⬜ Pass / ⬜ Fail | ⬜ Pass / ⬜ Fail | |
| Agent Discovery | ⬜ Pass / ⬜ Fail | ⬜ Pass / ⬜ Fail | |
| Helper Script | ⬜ N/A | ⬜ Pass / ⬜ Fail | |
| Identical Output | ⬜ Pass / ⬜ Fail | ⬜ Pass / ⬜ Fail | |
| Error Handling | ⬜ Pass / ⬜ Fail | ⬜ Pass / ⬜ Fail | |
| Documentation | ⬜ Pass / ⬜ Fail | ⬜ Pass / ⬜ Fail | |
| Performance | ⬜ N/A | ⬜ Pass / ⬜ Fail | |

## Issues Found

Document any issues discovered:
```
Issue 1:
- Description:
- CLI affected:
- Severity:
- Workaround:

Issue 2:
...
```

## Sign-off

- [ ] All critical tests pass
- [ ] Both CLIs functional
- [ ] Documentation accurate
- [ ] Ready for production use

Tested by: _______________  
Date: _______________
