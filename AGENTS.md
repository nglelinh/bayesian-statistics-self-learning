# AGENTS.md - Development Guide for AI Coding Agents

This document provides essential information for AI coding agents working in this repository.

## Project Overview

**Bayesian Statistics - Self Learning Course**: A comprehensive Vietnamese educational course website built with Jekyll 4.3.0, offering 33 lessons in Bayesian statistics based on Statistical Rethinking by Richard McElreath. The project includes 400+ illustrations, 150+ exercises, and 7 lab solutions.

**Tech Stack**: Jekyll (Ruby), Python (PyMC/NumPy/Matplotlib), JavaScript, Markdown

---

## Build/Test Commands

### Local Development

```bash
# Install dependencies
bundle install

# Serve Jekyll site locally (main workflow)
bundle exec jekyll serve
# Visit: http://127.0.0.1:4000/bayesian-statistics-self-learning/

# Build site without serving
bundle exec jekyll build --verbose

# Alternative: Docker
docker-compose up
```

### Python Environment

```bash
# Install Python dependencies (for exercises and labs)
pip install numpy matplotlib scipy seaborn pymc arviz pandas jupyter

# Verify installation
python -c "import pymc, arviz; print('✅ Ready')"

# Run Jupyter notebooks
jupyter notebook exercises/Chapter01_Bayesian_Inference_Exercises.ipynb
```

### Testing

**⚠️ No automated tests exist.** Manual validation only:
- **Website**: Build Jekyll and visually inspect at localhost:4000
- **Content**: Check markdown renders correctly, math formulas display, images load
- **Notebooks**: Execute cells in Jupyter to verify Python code
- **Links**: Manually verify no broken links/images

---

## Code Style Guidelines

### General Principles

1. **No automated formatters configured** - Follow manual conventions below
2. **Bilingual**: All content should exist in both `en/` and `vi/` directories
3. **Pedagogical focus**: Prioritize clarity and teaching over code optimization
4. **No test coverage requirements** - This is an educational project

### Markdown (.md files)

```markdown
# Use proper heading hierarchy (H1 → H2 → H3)

- Add blank lines between paragraphs
- Use code blocks with syntax highlighting
- Number mathematical formulas clearly

# Front matter format for lecture content:
---
layout: post
title: "Lesson Title"
chapter: '01'
order: 0
owner: Nguyen Le Linh
lang: vi
categories:
  - chapter01
lesson_type: required
---
```

### LaTeX Math

```markdown
# Inline math: Use $$...$$ (NOT single $)
$$f(x) = x^2$$

# Complex formulas: Use block math
$$
\begin{align}
f(x) &= x^2 \\
g(x) &= 2x
\end{align}
$$
```

### Python Code

**Style**: Follow standard Python conventions (no Black/Ruff configured)

```python
#!/usr/bin/env python3
"""
Module docstring explaining purpose
"""

import json  # Standard library first
import sys

import numpy as np  # Third-party imports
import matplotlib.pyplot as plt


def example_function(data, param1, param2=0.01):
    """
    Clear docstring with purpose explanation
    
    Args:
        data: Input data description
        param1: First parameter
        param2: Second parameter (default: 0.01)
    
    Returns:
        result: Processed result description
    """
    # Clear inline comments
    result = process_data(data, param1, param2)
    return result


# Use meaningful variable names
# Add blank lines between functions
# Comment complex logic
```

### Ruby Plugins

**Style**: Follow standard Ruby conventions (no RuboCop configured)

```ruby
module Jekyll
  class ExampleTag < Liquid::Tag
    def initialize(tag_name, param, tokens)
      super
      @param = param.strip
    end

    def render(context)
      # Implementation with clear logic
      site = context.registers[:site]
      return result
    end
  end
end

Liquid::Template.register_tag('example', Jekyll::ExampleTag)
```

### JavaScript

**Style**: Standard ES5/ES6 conventions (no ESLint configured)

```javascript
// Use clear function names
function handleSidebarToggle() {
  // Comment non-obvious logic
  const sidebar = document.querySelector('.sidebar');
  sidebar.classList.toggle('active');
}

// Prefer const/let over var when possible
const CONFIG = {
  timeout: 1000,
  retries: 3
};
```

### File Naming Conventions

```
# Lecture content: YYYY-MM-DD-lesson-title.md
2024-01-15-bayesian-inference-intro.md

# Python scripts: lowercase_with_underscores.py
generate_chapter01_images.py
enhance_all_labs.py

# Notebooks: CamelCase with chapter prefix
Chapter01_Bayesian_Inference_Exercises.ipynb

# Images: descriptive lowercase with hyphens
bayesian-updating-process.png
```

---

## Import Guidelines

### Python Import Order

```python
# 1. Standard library
import os
import sys
import json

# 2. Third-party packages
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# 3. PyMC and Bayesian tools
import pymc as pm
import arviz as az

# 4. Local modules (if any)
from .utils import helper_function
```

### Jekyll/Ruby

```ruby
# Plugins should register properly
module Jekyll
  # Implementation
end

Liquid::Template.register_tag('tagname', Jekyll::TagClass)
```

---

## Error Handling

### Python

```python
# Use try-except for expected errors
try:
    result = risky_operation()
except ValueError as e:
    print(f"⚠️ Warning: {e}")
    result = default_value

# Let unexpected errors propagate for debugging
```

### Jekyll

```ruby
# Handle missing keys gracefully
value = site.config['key'] || default_value

# Check for nil before operations
if page['lang']
  current_lang = page['lang']
end
```

---

## Content Guidelines (from .cursor/rules/)

### Lecture Notes (lecture-notes-rule.mdc)

**Critical Requirements:**
1. **Narrative-driven style**: Write as if speaking in a 2-hour lecture
2. **NO bullet points** except where absolutely necessary
3. **Storytelling academic prose**: Each section flows logically into the next
4. **Motivation first**: Explain WHY before WHAT
5. **Models as generative stories**: Describe data-generating process before math
6. **Computational tools are secondary**: Reinforce ideas, never replace them
7. The writing should reflect the tone of a thoughtful professor explaining ideas to advanced students in a classroom.
8. Conceptual explanations should be reinforced with carefully chosen visual illustrations sourced from the internet

**Structure for every lecture:**
- Title (aligned with syllabus)
- Learning Objectives (paragraph, not list)
- Prerequisites (situate within prior knowledge)
- Introduction (create intellectual tension)
- Conceptual Development (slow, coherent progression)
- Models as Generative Stories (words → probability → code)
- Computational Realization (why simulation is needed)
- Interpretation and Insight
- Applications (real data analysis)
- Limitations and Extensions
- Exercises (3-5 reasoning-focused problems)
- References (cite Gelman's BDA3, Kruschke's DBDA)

### Practice Exercises (practice-rule.mdc)

**For Jupyter notebook assessments:**
1. **Context first**: Realistic applied scenario with clear data-generating story
2. **Progressive difficulty**: 4-6 tasks from basic to open-ended
3. **Python + PyMC**: Use PyMC for modeling, ArviZ for diagnostics
4. **Interpretation required**: Written questions about posteriors, priors, assumptions
5. **Skeleton code**: Provide structure, students fill implementation
6. **Emphasize reasoning**: Model specification, checking, criticism over computation

### Math Formulas (math-formula-rule.mdc)

**Format:**
1. **Formula/Theorem**: State clearly
2. **Explanation**: Brief description
3. **Derivation/Proof**: Step-by-step in LaTeX
4. **Example**: Simple numerical or data science application
5. **Brevity**: Under 500 words per formula
6. **Use $$ not $**: All math with double dollar signs

---

## Directory Structure

```
bayesian-statistics-self-learning/
├── contents/                  # Course content
│   ├── en/chapter{00-11}/    # English lessons
│   └── vi/chapter{00-11}/    # Vietnamese lessons (primary)
├── exercises/                 # 8 Jupyter notebooks (150+ problems)
├── labs/                      # 7 lab exercises with solutions
├── img/chapter_img/          # 400+ illustrations
├── _plugins/                  # Jekyll plugins (multilang support)
├── _layouts/                  # Jekyll templates
├── _includes/                 # Jekyll partials
├── public/                    # Static assets (css/, js/)
├── _config.yml               # Jekyll configuration
├── Gemfile                   # Ruby dependencies
└── docker-compose.yml        # Docker setup
```

---

## Contribution Workflow

### Adding Content

```bash
# 1. Create branch
git checkout -b feature/chapter-XX-new-topic

# 2. Add content in BOTH languages
# - contents/en/chapterXX/_posts/YYYY-MM-DD-title.md
# - contents/vi/chapterXX/_posts/YYYY-MM-DD-title.md

# 3. Test locally
bundle exec jekyll serve

# 4. Verify checklist:
# [ ] All pages load correctly
# [ ] No broken links/images
# [ ] Math formulas render (MathJax)
# [ ] Responsive on mobile
# [ ] Language switching works
# [ ] Both EN and VI versions exist

# 5. Commit and push
git add .
git commit -m "Add chapter XX: Topic name"
git push origin feature/chapter-XX-new-topic
```

### Modifying Python Scripts

```bash
# 1. Test script execution
python img/chapter_img/chapter01/generate_chapter01_images.py

# 2. Verify images generated correctly
ls -la img/chapter_img/chapter01/*.png

# 3. Commit changes
git commit -m "Update image generation for chapter 01"
```

### Jekyll Plugins

```bash
# 1. Add plugin to _plugins/
# 2. Register properly (Liquid::Template.register_tag)
# 3. Test thoroughly with jekyll serve
# 4. Update documentation
```

---

## Key Constraints

1. **No push to remote without explicit user request**
2. **No automated code quality tools** (Black, Ruff, ESLint) - use manual style
3. **Bilingual requirement**: Content must exist in both en/ and vi/
4. **Pedagogical priority**: Teaching clarity > code elegance
5. **No empty commits**: Only commit when there are actual changes
6. **MathJax dependency**: All math must render with $$ delimiters

---

## Deployment

**GitHub Actions**: Automatic deployment on push to `main`

```yaml
# .github/workflows/jekyll.yml
# - Ruby 3.1
# - Jekyll build → GitHub Pages
# - Available at: https://username.github.io/bayesian-statistics-self-learning/
```

**Manual deployment**: Push to main branch - CI/CD handles the rest.

---

## Common Tasks

### Generate Chapter Images
```bash
cd img/chapter_img/chapter01
python generate_chapter01_images.py
```

### Add New Lesson
```bash
# Create in both languages with proper front matter
touch contents/vi/chapter01/_posts/2024-01-15-new-lesson.md
touch contents/en/chapter01/_posts/2024-01-15-new-lesson.md
```

### Test Notebook
```bash
jupyter notebook exercises/Chapter01_Bayesian_Inference_Exercises.ipynb
# Execute all cells and verify no errors
```

---

**Version**: 0.0.1  
**Last Updated**: 2026-03-08  
**Maintained by**: Nguyen Le Linh
