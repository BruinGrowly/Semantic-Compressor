# Using LJPW Semantic Analyzer with AI Chatbots

## Quick Start - For Users

### Method 1: Copy-Paste into Chat (Easiest!)

**Step 1:** Copy the entire contents of `ljpw_standalone.py` (it's a single file!)

**Step 2:** Paste it into your AI chatbot (ChatGPT, Claude, etc.) and say:

```
I've pasted the LJPW Semantic Analyzer code above.
Please analyze this code for me: [paste your code here]
```

The AI will run the analyzer and give you results!

---

### Method 2: Ask AI to Use It

Simply say to your AI chatbot:

```
Please analyze my code using the LJPW framework. Here's my code:

[paste code here]

Measure:
- Love (Safety): error handling, validation
- Justice (Structure): types, documentation
- Power (Performance): algorithms, efficiency
- Wisdom (Design): patterns, architecture
```

The AI understands the LJPW framework and can analyze your code!

---

## Integration Guide for AI Platforms

### ChatGPT Integration

**Method A: Direct Code Analysis**

```
User: "Run LJPW analysis on this code:
[paste code]"

ChatGPT: [Analyzes code using LJPW principles and provides scores]
```

**Method B: Upload ljpw_standalone.py**

1. Start new chat
2. Upload `ljpw_standalone.py`
3. Ask: "Please use this tool to analyze my code"

---

### Claude Integration

**Method A: Attach as Project Knowledge**

1. Create new project in Claude
2. Add `ljpw_standalone.py` to project knowledge
3. Now Claude can always analyze code with LJPW!

**Method B: Direct Request**

```
User: "Analyze my code using LJPW framework (Love, Justice, Power, Wisdom):
[code here]"

Claude: [Provides LJPW analysis]
```

---

### GitHub Copilot Chat Integration

In VS Code:

```
@workspace /analyze using LJPW framework
```

Or in chat:

```
Analyze this file using LJPW semantic analysis:
- Safety (Love)
- Structure (Justice)
- Performance (Power)
- Design (Wisdom)
```

---

### Cursor IDE Integration

1. Add `ljpw_standalone.py` to your project
2. In Cursor chat: `@Files analyze using LJPW`
3. Or: Select code → Right-click → "Chat" → "Analyze with LJPW"

---

## Custom GPT / Claude Project Setup

### Creating a "Code Quality Analyzer" GPT

**Instructions for GPT:**

```
You are a code quality analyzer using the LJPW framework.

LJPW measures 4 dimensions:
- Love (L): Safety, error handling, validation, null checks
- Justice (J): Structure, types, interfaces, documentation
- Power (P): Performance, algorithms, optimization, efficiency
- Wisdom (W): Design, patterns, architecture, modularity

Natural Equilibrium (optimal balance):
- L = 0.618
- J = 0.414
- P = 0.718
- W = 0.693

When analyzing code:
1. Count safety features (try/catch, validation, type checks)
2. Count structural features (types, docs, interfaces)
3. Count performance features (algorithms, caching, async)
4. Count design features (patterns, abstraction, modules)

5. Calculate scores (0-1.5 range)
6. Calculate health = 1 - distance_from_NE / 2
7. Generate actionable insights

Always provide:
- LJPW scores
- Health percentage
- Specific recommendations
- Comparison to Natural Equilibrium
```

**Knowledge Base:** Upload `ljpw_standalone.py`

**Conversation Starters:**
- "Analyze my code quality"
- "What's my LJPW score?"
- "How can I improve my code?"
- "Compare two code versions"

---

## API Integration (For Developers)

### Simple Flask API

Create `ljpw_api.py`:

```python
from flask import Flask, request, jsonify
from ljpw_standalone import SimpleCodeAnalyzer

app = Flask(__name__)
analyzer = SimpleCodeAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.json.get('code', '')
    result = analyzer.analyze(code)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
```

Then in your AI tool:

```python
import requests

code = "def hello(): print('hi')"
response = requests.post('http://localhost:5000/analyze',
                        json={'code': code})
print(response.json())
```

---

## Browser Extension Integration

### Bookmarklet for Quick Analysis

```javascript
javascript:(function(){
  var code = prompt("Paste code to analyze:");
  if(code){
    // Call LJPW API or open analysis page
    window.open('https://your-ljpw-analyzer.com?code=' + encodeURIComponent(code));
  }
})();
```

Save as bookmark, click to analyze any code!

---

## Slack Bot Integration

```python
from slack_bolt import App
from ljpw_standalone import SimpleCodeAnalyzer

app = App(token="YOUR_TOKEN")
analyzer = SimpleCodeAnalyzer()

@app.command("/ljpw")
def analyze_code(ack, command):
    ack()
    code = command['text']
    result = analyzer.analyze(code)

    message = f"""
    LJPW Analysis:
    Love: {result['ljpw']['L']:.2f}
    Justice: {result['ljpw']['J']:.2f}
    Power: {result['ljpw']['P']:.2f}
    Wisdom: {result['ljpw']['W']:.2f}
    Health: {result['health']*100:.0f}%
    """

    app.client.chat_postMessage(
        channel=command['channel_id'],
        text=message
    )

app.start(3000)
```

Usage in Slack: `/ljpw def hello(): print('hi')`

---

## VS Code Extension

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "LJPW Analysis",
      "type": "shell",
      "command": "python",
      "args": ["ljpw_standalone.py", "analyze", "${file}"],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

Then: `Ctrl+Shift+P` → "Run Task" → "LJPW Analysis"

---

## Command Line Power User Guide

### Analyze Single File
```bash
python ljpw_standalone.py analyze mycode.py
```

### Analyze Directory
```bash
python ljpw_standalone.py analyze ./src
```

### Quick Snippet Analysis
```bash
python ljpw_standalone.py quick "def test(): pass"
```

### Save Results to JSON
```bash
python ljpw_standalone.py analyze ./src --save
```

### Pipe from stdin
```bash
cat mycode.py | python ljpw_standalone.py quick "$(cat)"
```

### Batch Analysis with Shell Script
```bash
#!/bin/bash
for file in src/**/*.py; do
  echo "Analyzing $file..."
  python ljpw_standalone.py analyze "$file"
done
```

---

## GitHub Actions Integration

Create `.github/workflows/ljpw.yml`:

```yaml
name: LJPW Code Quality Check

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Download LJPW Analyzer
        run: |
          wget https://raw.githubusercontent.com/YOUR_REPO/ljpw_standalone.py

      - name: Run LJPW Analysis
        run: |
          python ljpw_standalone.py analyze ./src --save

      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: ljpw-results
          path: ljpw_results.json
```

---

## Pre-commit Hook Integration

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "Running LJPW analysis on changed files..."

for file in $(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|java|rs)$'); do
  if [ -f "$file" ]; then
    result=$(python ljpw_standalone.py analyze "$file")

    # Extract health score
    health=$(echo "$result" | grep "Health Score" | grep -oP '\d+\.\d+')

    if (( $(echo "$health < 40" | bc -l) )); then
      echo "WARNING: $file has low health score ($health%)"
      echo "Consider improving code quality before committing"
    fi
  fi
done
```

Make executable: `chmod +x .git/hooks/pre-commit`

---

## Tips for AI Chat Integration

### 1. Be Specific in Your Requests

❌ Bad: "Check my code"

✅ Good: "Run LJPW analysis focusing on safety (Love) and structure (Justice)"

### 2. Request Comparison

```
Compare the LJPW scores of these two implementations:

Version A:
[code]

Version B:
[code]

Which is better balanced?
```

### 3. Ask for Improvement Suggestions

```
My code has low Justice score (0.3).
Suggest specific improvements to reach Natural Equilibrium (0.414).
```

### 4. Track Progress

```
I improved my code. Please re-analyze and compare to previous scores:

Previous: L=0.4, J=0.3, P=0.6, W=0.5
New code:
[paste]
```

---

## Example Conversations

### Example 1: Quick Check

```
User: "Analyze this with LJPW:
def process(data):
    return [x*2 for x in data]"

AI: "LJPW Analysis:
- Love (Safety): 0.0 - No error handling!
- Justice (Structure): 0.0 - Missing type hints
- Power (Performance): 0.2 - List comprehension is good
- Wisdom (Design): 0.1 - Minimal

Health: 38% - NEEDS IMPROVEMENT

Recommendations:
1. Add type hints: def process(data: List[int]) -> List[int]
2. Add validation: if not data: raise ValueError
3. Add error handling: try/except
4. Add documentation"
```

### Example 2: Refactoring Guidance

```
User: "I'm refactoring. Which version has better LJPW balance?
[two code versions]"

AI: "LJPW Comparison:

Version A: L=0.3, J=0.2, P=0.8, W=0.4 (Health: 42%)
Version B: L=0.6, J=0.5, P=0.7, W=0.7 (Health: 73%)

Version B is significantly better:
- 2x better safety
- 2.5x better structure
- Better balanced (closer to NE)

Recommend Version B with these tweaks:
- Reduce Power slightly (currently 0.7, target 0.718)
- Maintain other dimensions"
```

---

## Sharing Results

### Markdown Format for Issues/PRs

```markdown
## LJPW Code Quality Report

**File:** `src/processor.py`

| Dimension | Score | Target | Status |
|-----------|-------|--------|--------|
| Love (Safety) | 0.45 | 0.62 | ⚠️ Below target |
| Justice (Structure) | 0.51 | 0.41 | ✅ Above target |
| Power (Performance) | 0.82 | 0.72 | ⚠️ Too high |
| Wisdom (Design) | 0.68 | 0.69 | ✅ On target |

**Health Score:** 65% (FAIR)

**Recommendations:**
- Add input validation (boost Love)
- Optimize complex loops (reduce Power)
- Consider abstracting repeated logic (boost Wisdom)
```

---

## Getting Started Checklist

- [ ] Download `ljpw_standalone.py`
- [ ] Test with: `python ljpw_standalone.py quick "print('test')"`
- [ ] Try analyzing a real file
- [ ] Share with your AI chatbot
- [ ] Set up VS Code task (optional)
- [ ] Add to pre-commit hooks (optional)
- [ ] Create custom GPT/Claude project (optional)
- [ ] Share results with team

---

## Support & Community

- **GitHub:** [Link to your repo]
- **Issues:** Report bugs or suggest features
- **Discussions:** Share your LJPW scores and improvements
- **License:** MIT - Free forever!

---

## Quick Reference Card

```
LJPW Framework Cheat Sheet

L (Love) = Safety
- Error handling (try/catch)
- Validation (check/verify)
- Null safety (Optional/Maybe)
Target: 0.618

J (Justice) = Structure
- Type annotations
- Documentation
- Interfaces
Target: 0.414

P (Power) = Performance
- Algorithms (sort/search)
- Async/parallel
- Optimization
Target: 0.718

W (Wisdom) = Design
- Abstraction
- Design patterns
- Modularity
Target: 0.693

Health = 1 - distance_from_NE / 2

80%+ = EXCELLENT
60-80% = GOOD
40-60% = FAIR
<40% = NEEDS WORK
```

---

**Remember:** LJPW is free for everyone, forever. Share it, improve it, use it to write better code!
