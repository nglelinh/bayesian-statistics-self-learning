# Interactive DAG Explorer

**Version**: 2.0  
**Date**: March 10, 2026  
**Author**: Nguyen Le Linh  
**Language**: Vietnamese (Tiếng Việt)

## 📖 Giới thiệu

Interactive DAG Explorer là một công cụ web tương tác được thiết kế để giúp sinh viên học và thực hành **Causal Inference** (Suy luận Nhân quả) thông qua việc vẽ và phân tích **Directed Acyclic Graphs (DAGs)**.

Công cụ này là một phần của khóa học **Bayesian Statistics Self-Learning Course**, đặc biệt hữu ích cho **Chương 5: Hồi quy Đa biến và Tư duy Nhân quả**.

## 🎯 Mục đích

Công cụ này giúp sinh viên:

1. **Vẽ DAG trực quan** - Tạo và chỉnh sửa DAGs với giao diện kéo thả đơn giản
2. **Xác định Adjustment Sets** - Tự động tìm ra các biến cần control để ước lượng causal effect
3. **Phát hiện Backdoor Paths** - Nhận diện các non-causal paths giữa treatment và outcome
4. **Hiểu Node Roles** - Phân biệt confounders, mediators, và colliders
5. **Kiểm tra DAG Properties** - Xác nhận DAG có acyclic không, đếm nodes/edges, phát hiện cycles

## ✨ Tính năng

### Phiên bản 2.0 (Mới)

#### ✅ Cải tiến Algorithms (Phiên bản 2.0)
- **Improved Backdoor Criterion**: Thuật toán backdoor criterion hoàn chỉnh với collider detection
- **Multiple Adjustment Sets**: Tìm tất cả valid adjustment sets (không chỉ một)
- **Minimal Adjustment Set**: Tự động chọn set nhỏ nhất (ít biến nhất)
- **D-separation Algorithm**: Thuật toán d-separation đúng chuẩn với path blocking logic
- **Descendant Detection**: Không cho phép condition trên descendants của treatment

#### 🎨 Cải tiến UI/UX
- **Node Deletion**: Click phải (right-click) vào node hoặc chọn và nhấn Delete/Backspace
- **Edge Deletion**: Click vào edge để xóa (có confirmation)
- **Undo/Redo**: Ctrl+Z / Ctrl+Y hoặc dùng buttons
- **Auto Layout**: Tự động sắp xếp nodes theo cấu trúc phân cấp (hierarchical layout)
- **Node Selection**: Chọn node bằng click (highlighted border)
- **Drag & Drop**: Di chuyển nodes tự do trên canvas
- **Cycle Detection**: Cảnh báo khi DAG có cycle (vi phạm tính acyclic)

#### 📊 Cải tiến Analysis Panel
- **Detailed Adjustment Set Results**: Hiển thị explanation, minimal set, và alternative sets
- **Visual Feedback**: Color-coded results (green = no adjustment needed, red = no valid set)
- **Multiple Valid Sets**: Hiển thị tối đa 5 valid adjustment sets
- **Enhanced Node Roles**: Badges cho confounders, mediators, colliders

### Tính năng Cơ bản

#### 🛠️ Công cụ Vẽ DAG
- **Add Node**: Nhập tên node và click "Add Node"
- **Add Edge**: Chọn From/To nodes và click "Add Edge"
- **Load Examples**: 5 DAG examples có sẵn (Fork, Chain, Collider, Simpson's Paradox, Complex)
- **Clear Canvas**: Xóa toàn bộ DAG để bắt đầu lại

#### 📊 Phân tích Causal
- **Treatment/Outcome Selection**: Chọn treatment (X) và outcome (Y) để phân tích
- **Adjustment Set Computation**: Tự động tính toán adjustment sets dựa trên backdoor criterion
- **Backdoor Path Detection**: Liệt kê tất cả backdoor paths từ X đến Y
- **Node Role Identification**: Xác định vai trò của từng node

#### 💾 Export
- **Export PNG**: Export DAG dưới dạng hình ảnh (yêu cầu screenshot tool)
- **Export Code**: Generate PyMC code skeleton từ DAG structure

## 🖱️ Hướng dẫn Sử dụng

### 1. Tạo DAG

#### Cách 1: Thêm từng Node và Edge
```
1. Nhập tên node (ví dụ: "Age", "Income", "Education")
2. Click "Add Node"
3. Lặp lại cho tất cả nodes
4. Chọn "From" node và "To" node
5. Click "Add Edge" để tạo mũi tên
```

#### Cách 2: Load Example DAG
```
1. Click một trong các buttons:
   - "Fork (Confounder)" - Z → X, Z → Y
   - "Chain (Mediator)" - X → M → Y
   - "Collider" - X → C ← Y
   - "Simpson's Paradox" - Confounding example
   - "Complex Example" - Multi-node DAG
2. Sau đó có thể chỉnh sửa thêm
```

### 2. Chỉnh sửa DAG

- **Di chuyển node**: Kéo thả node đến vị trí mới
- **Xóa node**: 
  - Cách 1: Right-click vào node
  - Cách 2: Click chọn node (sẽ có border đỏ), nhấn Delete hoặc Backspace
- **Xóa edge**: Click vào mũi tên (edge sẽ highlight màu đỏ khi hover)
- **Sắp xếp tự động**: Click "Auto Layout" để tự động sắp xếp nodes theo hierarchy
- **Undo/Redo**: 
  - Cách 1: Ctrl+Z (undo), Ctrl+Y (redo)
  - Cách 2: Click buttons "↶ Undo" / "↷ Redo"

### 3. Phân tích Causal Effect

```
1. Chọn Treatment (X) từ dropdown "Treatment (X)"
2. Chọn Outcome (Y) từ dropdown "Outcome (Y)"
3. Xem kết quả phân tích tự động:
   
   📍 Minimal Adjustment Set
   - Variables cần control để estimate causal effect đúng
   - Có thể có nhiều valid sets (hiển thị 5 sets đầu tiên)
   - Empty set {} = không cần adjustment
   
   📍 Backdoor Paths
   - Danh sách tất cả non-causal paths từ X đến Y
   - Mỗi path bắt đầu bằng mũi tên vào X
   
   📍 Node Roles
   - Confounders: Nodes ảnh hưởng đến cả X và Y
   - Mediators: Nodes trên đường từ X đến Y
   - Colliders: Nodes có 2+ incoming edges
   
   📍 DAG Properties
   - Node count, Edge count
   - Is Acyclic: Yes/No (có cycle không?)
```

### 4. Export và Chia sẻ

- **Export PNG**: Sử dụng screenshot tool của browser (Cmd+Shift+4 trên Mac)
- **Export Code**: Click "Export Code" để xem PyMC skeleton code

## 📚 Ví dụ DAG có sẵn

### 1. Fork (Confounder)
```
      Z
     ↙ ↘
    X   Y
```
- **Confounding**: Z là common cause của X và Y
- **Adjustment Set**: {Z}
- **Backdoor Path**: X ← Z → Y

### 2. Chain (Mediator)
```
X → M → Y
```
- **Mediation**: M nằm giữa X và Y
- **Adjustment Set**: {} (empty) nếu muốn total effect
- **Adjustment Set**: {M} nếu muốn direct effect

### 3. Collider
```
    X   Y
     ↘ ↙
      C
```
- **Collider**: C có 2 incoming edges
- **Adjustment Set**: {} (empty)
- **Lưu ý**: KHÔNG condition trên C (sẽ mở backdoor path!)

### 4. Simpson's Paradox
```
      U
     ↙ ↘
    T   Y
     ↘ ↙
```
- **Confounding + Direct Effect**: U confounds T→Y relationship
- **Adjustment Set**: {U}
- **Simpson's Paradox**: Raw correlation ≠ causal effect

### 5. Complex Example
```
    U       V
   ↙ ↘     ↙ ↘
  X   →  M  →  Y
            ↓
            Z
```
- **Multiple Paths**: Direct + mediated paths
- **Multiple Confounders**: U và V
- **Adjustment Set**: Depends on question

## 🧠 Lý thuyết: Backdoor Criterion

### Backdoor Path là gì?

**Backdoor path** là một path từ treatment X đến outcome Y mà:
1. Bắt đầu bằng mũi tên **đi vào** X (không phải đi ra)
2. Có thể đi ngược chiều hoặc xuôi chiều
3. Tạo ra non-causal association giữa X và Y

**Ví dụ**:
```
    U
   ↙ ↘
  X   Y
   ↘ ↙
    M
```
- Backdoor path: X ← U → Y (tạo confounding)
- Direct path: X → M → Y (causal)

### Backdoor Criterion

Để ước lượng causal effect của X lên Y, ta cần tìm một **adjustment set** Z sao cho:

1. **Block all backdoor paths**: Mọi backdoor path từ X đến Y đều bị blocked khi condition trên Z
2. **Not a descendant**: Z không chứa descendants của X (tránh post-treatment bias)

### Path Blocking Rules

Một path bị **blocked** khi:

1. **Non-collider**: Có một node trên path KHÔNG phải collider và node đó trong Z
   ```
   X ← U → Y    # Blocked if U ∈ Z
   ```

2. **Collider**: Có một collider trên path và collider đó KHÔNG trong Z (và descendants cũng không trong Z)
   ```
   X → C ← Y    # Blocked if C ∉ Z and desc(C) ∉ Z
   ```

## 💻 Technical Details

### Implementation

- **Frontend**: Pure HTML5 + CSS3 + Vanilla JavaScript (no framework dependencies)
- **DAG Library**: Dagitty.js 3.1.0 (optional, for advanced features)
- **Canvas**: SVG-based rendering with dynamic manipulation
- **Layout Algorithm**: Hierarchical layout using BFS topological ordering
- **State Management**: History stack (max 50 states) for undo/redo

### Algorithms

#### 1. Backdoor Path Finding
```javascript
// Explores paths starting with incoming edge to treatment
function findBackdoorPaths(treatment, outcome) {
    // DFS from treatment going backward first
    // Then can go forward along the path
    // Returns all paths from treatment to outcome
}
```

#### 2. Adjustment Set Computation
```javascript
function findAllAdjustmentSets(treatment, outcome, backdoorPaths) {
    // 1. Get candidate nodes (exclude treatment, outcome, descendants)
    // 2. Test all subsets (2^n, limited to n≤10 for performance)
    // 3. Check if subset blocks all backdoor paths
    // 4. Return minimal sets first
}
```

#### 3. Path Blocking Check
```javascript
function isPathBlocked(pathNodes, conditionSet) {
    // For each node on path:
    //   - If collider: blocked unless conditioned
    //   - If non-collider: blocked if conditioned
}
```

#### 4. Auto Layout
```javascript
function autoLayout() {
    // 1. Calculate in-degree for each node
    // 2. BFS to assign levels (topological ordering)
    // 3. Position nodes in hierarchical structure
    // 4. Equal spacing within each level
}
```

### Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**Keyboard Shortcuts**:
- `Ctrl+Z` / `Cmd+Z`: Undo
- `Ctrl+Y` / `Cmd+Y`: Redo
- `Delete` / `Backspace`: Delete selected node
- `Right-click`: Context menu (delete node)

## 📂 File Structure

```
tools/dag-explorer/
├── README.md                  # This file (Vietnamese documentation)
├── standalone.html            # Standalone version (enhanced v2.0)
└── index.html                 # Jekyll-integrated version (basic)

tools/
└── dag-explorer-page.html     # Jekyll wrapper page (iframe embed)
```

## 🔗 Integration with Jekyll

### Access URLs

1. **Standalone Version** (Full Features):
   ```
   http://localhost:4000/bayesian-statistics-self-learning/tools/dag-explorer/standalone.html
   ```

2. **Jekyll Integrated Version**:
   ```
   http://localhost:4000/bayesian-statistics-self-learning/tools/dag-explorer-page/
   ```

3. **Direct Link from Chapter 5**:
   - Add link to lesson markdown files in Chapter 05

### Embedding in Lesson

To embed in a lesson, add this to markdown:

```markdown
## 🎯 Interactive Exercise

Hãy thử [Interactive DAG Explorer]({{ site.baseurl }}/tools/dag-explorer/standalone.html) 
để vẽ DAG của bài toán này!

<iframe src="{{ site.baseurl }}/tools/dag-explorer/standalone.html" 
        width="100%" height="800px" style="border: 1px solid #ddd;">
</iframe>
```

## 🎓 Pedagogical Use Cases

### 1. Lecture Demonstration
- Instructor vẽ DAG trực tiếp trong lúc giảng
- Sinh viên thấy real-time adjustment set computation
- Thảo luận về different causal questions

### 2. Homework Exercises
```
Bài tập: Vẽ DAG cho các tình huống sau:

1. Education → Income, Age → Income, Age → Education
   - Tìm adjustment set để estimate effect của Education lên Income
   
2. Smoking → Cancer, Gene → Smoking, Gene → Cancer
   - Có nên adjust cho Gene không? Tại sao?
   
3. Treatment → Recovery, Hospital Quality → Treatment, 
   Hospital Quality → Recovery, Severity → Hospital Quality
   - Adjustment set là gì? Giải thích.
```

### 3. Exam Questions
- Cho DAG, yêu cầu sinh viên identify adjustment sets
- Cho adjustment set, yêu cầu vẽ DAG tương ứng
- Phân tích Simpson's Paradox với DAG

### 4. Research Project
- Sinh viên vẽ DAG cho research question của mình
- Phân tích confounders và mediators
- Justify adjustment strategy

## 📖 References

### Recommended Reading

1. **Pearl, J. (2009)**. *Causality: Models, Reasoning and Inference* (2nd ed.)
   - Chapter 3: Causal Diagrams
   - Section 3.3: Backdoor Criterion

2. **Hernán, M. A., & Robins, J. M. (2020)**. *Causal Inference: What If*
   - Chapter 6: Graphical representation of causal effects
   - Chapter 7: Confounding

3. **McElreath, R. (2020)**. *Statistical Rethinking* (2nd ed.)
   - Chapter 5: The Many Variables & The Spurious Waffles
   - Chapter 6: The Haunted DAG & The Causal Terror

4. **Dagitty Documentation**: http://dagitty.net/learn/

### Related Tools

- **Dagitty** (http://dagitty.net): More advanced DAG analysis (R/JavaScript)
- **ggdag** (R package): DAG visualization in R
- **DoWhy** (Python): Causal inference with DAG support

## 🐛 Known Issues & Limitations

### Current Limitations

1. **Performance**: Adjustment set computation is O(2^n) where n = number of candidate nodes
   - Limited to 10 candidate nodes for performance
   - For large DAGs, may not find all valid sets

2. **Export PNG**: Requires manual screenshot (no built-in SVG→PNG conversion)
   - Use browser screenshot tools
   - Or implement html2canvas library in future

3. **Mobile Support**: Touch drag-drop works but not optimized
   - Best experience on desktop/laptop

4. **No Server Backend**: All computation in browser
   - Cannot save DAGs to server
   - Use Export Code feature to save as text

### Future Enhancements (v3.0)

- [ ] Front-door criterion support
- [ ] Instrumental variables identification
- [ ] Conditional independencies display
- [ ] DAG comparison tool (compare two DAGs side-by-side)
- [ ] LaTeX export (TikZ code for papers)
- [ ] Save/load DAGs from local storage
- [ ] Collaboration features (share DAG URL)
- [ ] Mobile-optimized UI
- [ ] Unit tests for algorithms

## 📝 Version History

### Version 2.0 (March 10, 2026)
- ✅ Enhanced backdoor criterion algorithm with proper d-separation
- ✅ Multiple adjustment sets computation
- ✅ Node/edge deletion functionality
- ✅ Undo/redo with keyboard shortcuts
- ✅ Auto layout with hierarchical positioning
- ✅ Cycle detection and warning
- ✅ Improved UI with visual feedback
- ✅ Better adjustment set display with explanations

### Version 1.0 (March 9, 2026)
- Initial release
- Basic DAG drawing
- Simplified backdoor criterion
- 5 example DAGs
- Treatment/outcome selection
- Basic adjustment set computation

## 👨‍💻 Development

### Local Testing

1. Open `standalone.html` directly in browser
2. Or serve via Jekyll:
   ```bash
   bundle exec jekyll serve
   ```
3. Visit: http://localhost:4000/bayesian-statistics-self-learning/tools/dag-explorer/standalone.html

### Code Structure

```javascript
// Global State
let nodes = [];        // [{name, x, y}, ...]
let edges = [];        // [{from, to}, ...]
let history = [];      // State stack for undo/redo
let historyIndex = -1;

// Main Functions
- initCanvas()           // Setup SVG canvas
- addNode()              // Add node to DAG
- addEdge()              // Add edge to DAG
- renderDAG()            // Render SVG elements
- analyzeDAG()           // Compute causal analysis
- computeAdjustmentSet() // Backdoor criterion
- findBackdoorPaths()    // Path finding algorithm
- autoLayout()           // Hierarchical layout
- saveState()            // History management
- undo() / redo()        // State restoration
```

## 📧 Contact & Support

**Course Website**: https://nglelinh.github.io/bayesian-statistics-self-learning/

**Issues & Bug Reports**: Please report via GitHub Issues

**Course Instructor**: Nguyen Le Linh

---

**License**: MIT (Educational use)  
**Course**: Bayesian Statistics Self-Learning  
**Chapter**: 05 - Multiple Regression and Causal Thinking  
**Last Updated**: March 10, 2026
