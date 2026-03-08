"""
Generate cartoon-style images for Bài 2.3: Prior - Mã hóa Kiến thức Ban đầu
Enhanced version with storytelling about The Prior Debate
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np
import os

# Create output directory
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

def create_prior_debate_intro(output_dir):
    """Image 1: The Prior Debate - Professor Chen vs Dr. Roberts"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Cuộc Tranh luận Lịch sử về Prior', 
            fontsize=22, fontweight='bold', ha='center')
    ax.text(5, 9, 'Hội nghị Thống kê Quốc tế - Boston, 1985', 
            fontsize=14, ha='center', style='italic', color='gray')
    
    # Stage
    stage = FancyBboxPatch((0.5, 3), 9, 4, boxstyle="round,pad=0.1", 
                           edgecolor='black', facecolor='lightblue', linewidth=2)
    ax.add_patch(stage)
    
    # Dr. Roberts (Frequentist) - Left side, angry
    roberts_head = Circle((2.5, 5.5), 0.4, facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(roberts_head)
    roberts_body = FancyBboxPatch((2.1, 4.2), 0.8, 1.3, boxstyle="round,pad=0.05",
                                  edgecolor='black', facecolor='coral', linewidth=2)
    ax.add_patch(roberts_body)
    
    # Roberts' eyes (angry)
    ax.plot([2.35, 2.45], [5.55, 5.65], 'k-', linewidth=2)
    ax.plot([2.55, 2.65], [5.65, 5.55], 'k-', linewidth=2)
    
    # Roberts' mouth (frowning)
    ax.plot([2.3, 2.7], [5.3, 5.3], 'k-', linewidth=2)
    
    # Roberts' label
    ax.text(2.5, 3.8, 'Dr. Roberts\n(Frequentist)', 
            fontsize=11, ha='center', fontweight='bold')
    
    # Roberts' speech bubble
    bubble1 = FancyBboxPatch((0.3, 6), 2.5, 1.2, boxstyle="round,pad=0.1",
                            edgecolor='red', facecolor='mistyrose', linewidth=2)
    ax.add_patch(bubble1)
    ax.text(1.55, 6.6, '"Prior của anh là\nCHỦ QUAN!"', 
            fontsize=10, ha='center', fontweight='bold', color='darkred')
    
    # Professor Chen (Bayesian) - Right side, calm
    chen_head = Circle((7.5, 5.5), 0.4, facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(chen_head)
    chen_body = FancyBboxPatch((7.1, 4.2), 0.8, 1.3, boxstyle="round,pad=0.05",
                               edgecolor='black', facecolor='mediumseagreen', linewidth=2)
    ax.add_patch(chen_body)
    
    # Chen's eyes (calm)
    ax.plot(7.35, 5.55, 'ko', markersize=5)
    ax.plot(7.65, 5.55, 'ko', markersize=5)
    
    # Chen's mouth (smiling)
    smile = patches.Arc((7.5, 5.35), 0.3, 0.2, angle=0, theta1=200, theta2=340, 
                       color='black', linewidth=2)
    ax.add_patch(smile)
    
    # Chen's label
    ax.text(7.5, 3.8, 'Professor Chen\n(Bayesian)', 
            fontsize=11, ha='center', fontweight='bold')
    
    # Chen's speech bubble
    bubble2 = FancyBboxPatch((7.2, 6), 2.5, 1.2, boxstyle="round,pad=0.1",
                            edgecolor='green', facecolor='honeydew', linewidth=2)
    ax.add_patch(bubble2)
    ax.text(8.45, 6.6, '"Hãy xem xét\ntình huống này..."', 
            fontsize=10, ha='center', fontweight='bold', color='darkgreen')
    
    # Audience
    ax.text(5, 2.5, '👥 👥 👥 👥 👥 👥 👥 👥', fontsize=20, ha='center')
    ax.text(5, 2, '500 nhà nghiên cứu đang theo dõi', 
            fontsize=11, ha='center', style='italic', color='gray')
    
    # The question at stake
    question_box = FancyBboxPatch((1, 0.3), 8, 1.2, boxstyle="round,pad=0.1",
                                  edgecolor='purple', facecolor='lavender', linewidth=3)
    ax.add_patch(question_box)
    ax.text(5, 1.2, 'Câu hỏi:', fontsize=12, ha='center', fontweight='bold')
    ax.text(5, 0.8, 'Liệu có hợp lý khi BỎ QUA 50 nghiên cứu trước (10,000 bệnh nhân)', 
            fontsize=10, ha='center')
    ax.text(5, 0.5, 'và chỉ dựa vào 20 bệnh nhân hiện tại?', 
            fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_debate_intro.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: prior_debate_intro.png")

def create_what_is_prior(output_dir):
    """Image 2: What is Prior - Visual definition"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Prior là gì?', fontsize=20, fontweight='bold', ha='center')
    
    # Prior box (center)
    prior_box = FancyBboxPatch((3, 5), 4, 2.5, boxstyle="round,pad=0.15",
                               edgecolor='blue', facecolor='lightblue', linewidth=3)
    ax.add_patch(prior_box)
    ax.text(5, 7, 'PRIOR P(θ)', fontsize=18, ha='center', fontweight='bold')
    ax.text(5, 6.3, 'Phân phối xác suất mô tả', fontsize=11, ha='center')
    ax.text(5, 5.9, 'niềm tin về tham số θ', fontsize=11, ha='center')
    ax.text(5, 5.5, 'TRƯỚC KHI thấy dữ liệu', fontsize=11, ha='center', 
            style='italic', color='darkblue', fontweight='bold')
    
    # Sources of prior knowledge (arrows pointing to prior)
    sources = [
        (1, 3.5, 'Nghiên cứu\ntrước đó', 'green'),
        (2, 2, 'Lý thuyết\nkhoa học', 'orange'),
        (5, 1.5, 'Ràng buộc\nvật lý', 'red'),
        (8, 2, 'Kinh nghiệm\nchuyên môn', 'purple'),
        (9, 3.5, 'Thậm chí\n"không biết"', 'gray')
    ]
    
    for x, y, label, color in sources:
        # Source box
        source_box = FancyBboxPatch((x-0.6, y-0.4), 1.2, 0.8, boxstyle="round,pad=0.05",
                                    edgecolor=color, facecolor='white', linewidth=2)
        ax.add_patch(source_box)
        ax.text(x, y, label, fontsize=9, ha='center', va='center', color=color, fontweight='bold')
        
        # Arrow to prior
        arrow = FancyArrowPatch((x, y+0.4), (5, 5), 
                               arrowstyle='->', mutation_scale=20, 
                               linewidth=2, color=color, alpha=0.7)
        ax.add_patch(arrow)
    
    # Key insight box
    insight_box = FancyBboxPatch((0.5, 8.2), 9, 0.8, boxstyle="round,pad=0.1",
                                 edgecolor='gold', facecolor='lightyellow', linewidth=2)
    ax.add_patch(insight_box)
    ax.text(5, 8.6, '💡 Prior không phải "chủ quan tùy tiện" - nó là cách MINH BẠCH hóa kiến thức!', 
            fontsize=11, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'what_is_prior.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: what_is_prior.png")

def create_why_need_prior(output_dir):
    """Image 3: Why Need Prior - 4 benefits"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Tại sao Cần Prior? - 4 Lợi ích Quan trọng', 
            fontsize=18, fontweight='bold', ha='center')
    
    # 4 benefits in quadrants
    benefits = [
        {
            'pos': (1.5, 7, 3, 2),
            'title': '1. Kết hợp Thông tin',
            'desc': 'Kết hợp kiến thức từ\nnghiên cứu trước + dữ liệu mới',
            'icon': '📚',
            'color': 'lightblue'
        },
        {
            'pos': (5.5, 7, 3, 2),
            'title': '2. Regularization',
            'desc': 'Ổn định ước lượng\nkhi dữ liệu ít',
            'icon': '🛡️',
            'color': 'lightgreen'
        },
        {
            'pos': (1.5, 4, 3, 2),
            'title': '3. Minh bạch',
            'desc': 'Giả định rõ ràng,\ncó thể kiểm tra',
            'icon': '🔍',
            'color': 'lightyellow'
        },
        {
            'pos': (5.5, 4, 3, 2),
            'title': '4. Suy luận Tuần tự',
            'desc': 'Posterior hôm nay =\nPrior ngày mai',
            'icon': '🔄',
            'color': 'lightcoral'
        }
    ]
    
    for benefit in benefits:
        x, y, w, h = benefit['pos']
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=benefit['color'], linewidth=2)
        ax.add_patch(box)
        
        ax.text(x + w/2, y + h - 0.4, benefit['icon'], fontsize=30, ha='center')
        ax.text(x + w/2, y + h - 0.9, benefit['title'], 
                fontsize=12, ha='center', fontweight='bold')
        ax.text(x + w/2, y + 0.5, benefit['desc'], 
                fontsize=10, ha='center', va='center')
    
    # Example: Regularization with coin flip
    example_box = FancyBboxPatch((0.5, 0.5), 9, 3, boxstyle="round,pad=0.15",
                                 edgecolor='purple', facecolor='lavender', linewidth=2)
    ax.add_patch(example_box)
    
    ax.text(5, 3, 'Ví dụ: Tung đồng xu 3 lần, cả 3 lần Ngửa', 
            fontsize=13, ha='center', fontweight='bold')
    
    # Without prior
    ax.text(2.5, 2.2, '❌ Không có Prior:', fontsize=11, ha='center', fontweight='bold', color='red')
    ax.text(2.5, 1.8, 'MLE = 1.0 (100% Ngửa)', fontsize=10, ha='center')
    ax.text(2.5, 1.4, '→ KHÔNG HỢP LÝ!', fontsize=10, ha='center', color='red', fontweight='bold')
    
    # Arrow
    arrow = FancyArrowPatch((3.5, 1.8), (4.5, 1.8), 
                           arrowstyle='->', mutation_scale=30, 
                           linewidth=3, color='green')
    ax.add_patch(arrow)
    
    # With prior
    ax.text(7.5, 2.2, '✅ Có Prior Beta(2,2):', fontsize=11, ha='center', fontweight='bold', color='green')
    ax.text(7.5, 1.8, 'Posterior mean ≈ 0.71', fontsize=10, ha='center')
    ax.text(7.5, 1.4, '→ HỢP LÝ HƠN!', fontsize=10, ha='center', color='green', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'why_need_prior.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: why_need_prior.png")

def create_prior_types_spectrum(output_dir):
    """Image 4: Prior Types Spectrum"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Các Loại Prior: Từ Không Thông tin đến Có Thông tin', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Spectrum arrow
    arrow = FancyArrowPatch((1, 7), (9, 7), 
                           arrowstyle='<->', mutation_scale=30, 
                           linewidth=4, color='purple')
    ax.add_patch(arrow)
    
    ax.text(1, 7.5, 'Không biết gì', fontsize=11, ha='center', style='italic')
    ax.text(9, 7.5, 'Biết rất nhiều', fontsize=11, ha='center', style='italic')
    
    # Three types
    types = [
        {
            'x': 2,
            'name': 'Uninformative\n(Flat)',
            'example': 'Beta(1,1)',
            'desc': '"Tôi không\nbiết gì"',
            'color': 'gray',
            'knowledge': 'KHÔNG CÓ'
        },
        {
            'x': 5,
            'name': 'Weakly\nInformative',
            'example': 'Beta(2,2)',
            'desc': '"Tôi biết\nmột chút"',
            'color': 'steelblue',
            'knowledge': 'YẾU'
        },
        {
            'x': 8,
            'name': 'Strongly\nInformative',
            'example': 'Beta(50,50)',
            'desc': '"Tôi biết\nkhá nhiều"',
            'color': 'darkred',
            'knowledge': 'MẠNH'
        }
    ]
    
    for t in types:
        # Box
        box = FancyBboxPatch((t['x']-0.8, 3.5), 1.6, 3, boxstyle="round,pad=0.1",
                            edgecolor=t['color'], facecolor='white', linewidth=3)
        ax.add_patch(box)
        
        # Content
        ax.text(t['x'], 6, t['name'], fontsize=11, ha='center', fontweight='bold', color=t['color'])
        ax.text(t['x'], 5.4, t['example'], fontsize=10, ha='center', style='italic')
        ax.text(t['x'], 4.7, t['desc'], fontsize=9, ha='center')
        ax.text(t['x'], 4, f'Kiến thức:\n{t["knowledge"]}', 
                fontsize=9, ha='center', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor=t['color'], alpha=0.3))
        
        # Dot on spectrum
        ax.plot(t['x'], 7, 'o', markersize=15, color=t['color'], markeredgecolor='black', markeredgewidth=2)
    
    # Recommendation box
    rec_box = FancyBboxPatch((1, 0.5), 8, 2.5, boxstyle="round,pad=0.15",
                             edgecolor='gold', facecolor='lightyellow', linewidth=3)
    ax.add_patch(rec_box)
    
    ax.text(5, 2.5, '🎯 Khuyến nghị: Bắt đầu với WEAKLY INFORMATIVE', 
            fontsize=13, ha='center', fontweight='bold')
    ax.text(5, 2, '✅ Loại trừ giá trị cực đoan', fontsize=10, ha='center')
    ax.text(5, 1.6, '✅ Vẫn để dữ liệu có ảnh hưởng lớn', fontsize=10, ha='center')
    ax.text(5, 1.2, '✅ Lựa chọn mặc định tốt trong nhiều tình huống', fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_types_spectrum.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: prior_types_spectrum.png")

def create_combining_information(output_dir):
    """Image 5: Combining Information from Multiple Sources"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Kết hợp Thông tin từ Nhiều Nguồn', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Prior (top) - combining multiple sources
    prior_circle = Circle((5, 7), 1, facecolor='lightblue', edgecolor='blue', linewidth=3)
    ax.add_patch(prior_circle)
    ax.text(5, 7, 'PRIOR\nP(θ)', fontsize=12, ha='center', fontweight='bold')
    
    # Multiple sources feeding into prior
    sources = [
        (2, 8.5, '50 nghiên cứu\ntrước\n(10,000 BN)', 'green'),
        (8, 8.5, 'Lý thuyết\nsinh học', 'orange'),
        (1.5, 6, 'Ràng buộc:\n20% < θ < 95%', 'red'),
        (8.5, 6, 'Kinh nghiệm\nlâm sàng', 'purple')
    ]
    
    for x, y, label, color in sources:
        # Source box
        source_box = FancyBboxPatch((x-0.5, y-0.5), 1, 1, boxstyle="round,pad=0.05",
                                    edgecolor=color, facecolor='white', linewidth=2)
        ax.add_patch(source_box)
        ax.text(x, y, label, fontsize=8, ha='center', va='center', color=color, fontweight='bold')
        
        # Arrow to prior
        arrow = FancyArrowPatch((x, y-0.5), (5, 7-0.8), 
                               arrowstyle='->', mutation_scale=15, 
                               linewidth=2, color=color, alpha=0.7)
        ax.add_patch(arrow)
    
    # Likelihood (middle)
    likelihood_circle = Circle((5, 4.5), 1, facecolor='lightgreen', edgecolor='green', linewidth=3)
    ax.add_patch(likelihood_circle)
    ax.text(5, 4.5, 'LIKELIHOOD\nP(D|θ)', fontsize=12, ha='center', fontweight='bold')
    ax.text(5, 3.2, 'Dữ liệu MỚI:\n20 bệnh nhân', fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    # Multiplication
    ax.text(5, 5.7, '×', fontsize=30, ha='center', fontweight='bold')
    
    # Arrow down
    arrow_down = FancyArrowPatch((5, 3.5), (5, 2.2), 
                                arrowstyle='->', mutation_scale=30, 
                                linewidth=4, color='purple')
    ax.add_patch(arrow_down)
    
    # Posterior (bottom)
    posterior_box = FancyBboxPatch((3, 0.5), 4, 1.5, boxstyle="round,pad=0.15",
                                   edgecolor='purple', facecolor='plum', linewidth=3)
    ax.add_patch(posterior_box)
    ax.text(5, 1.5, 'POSTERIOR P(θ|D)', fontsize=14, ha='center', fontweight='bold')
    ax.text(5, 1, 'Kết hợp CẢ HAI nguồn thông tin!', fontsize=11, ha='center')
    
    # Comparison box
    comp_box = FancyBboxPatch((0.2, 2.5), 4, 1.2, boxstyle="round,pad=0.1",
                              edgecolor='red', facecolor='mistyrose', linewidth=2)
    ax.add_patch(comp_box)
    ax.text(2.2, 3.3, '❌ Frequentist:', fontsize=10, ha='center', fontweight='bold', color='red')
    ax.text(2.2, 2.9, 'Bỏ qua 10,000 BN,\nchỉ dùng 20 BN', fontsize=9, ha='center')
    
    comp_box2 = FancyBboxPatch((5.8, 2.5), 4, 1.2, boxstyle="round,pad=0.1",
                               edgecolor='green', facecolor='honeydew', linewidth=2)
    ax.add_patch(comp_box2)
    ax.text(7.8, 3.3, '✅ Bayesian:', fontsize=10, ha='center', fontweight='bold', color='green')
    ax.text(7.8, 2.9, 'Kết hợp cả hai\nmột cách có nguyên tắc', fontsize=9, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'combining_information.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: combining_information.png")

def create_addressing_subjectivity(output_dir):
    """Image 6: Addressing Subjectivity Concerns"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Giải quyết Lo ngại về "Tính Chủ quan" của Prior', 
            fontsize=18, fontweight='bold', ha='center')
    
    # 4 concerns and responses
    concerns = [
        {
            'y': 7.5,
            'concern': '"Prior quá chủ quan!"',
            'response': 'Mọi phân tích đều có giả định.\nPrior làm giả định MINH BẠCH!',
            'icon': '🔍'
        },
        {
            'y': 5.5,
            'concern': '"Prior có thể bị lạm dụng!"',
            'response': 'Đúng vậy! Nhưng Frequentist cũng thế\n(p-hacking, HARKing).\nGiải pháp: Minh bạch + Peer review',
            'icon': '⚠️'
        },
        {
            'y': 3.5,
            'concern': '"Dữ liệu không được tự nói!"',
            'response': 'Dữ liệu SẼ áp đảo prior\nnếu đủ mạnh!',
            'icon': '💪'
        },
        {
            'y': 1.5,
            'concern': '"Làm sao biết prior đúng?"',
            'response': 'Không cần prior "đúng"!\nChỉ cần: hợp lý + minh bạch\n+ sensitivity analysis',
            'icon': '✅'
        }
    ]
    
    for concern in concerns:
        # Concern (left)
        concern_box = FancyBboxPatch((0.5, concern['y']-0.4), 3.5, 0.8, boxstyle="round,pad=0.1",
                                     edgecolor='red', facecolor='mistyrose', linewidth=2)
        ax.add_patch(concern_box)
        ax.text(2.25, concern['y'], concern['concern'], 
                fontsize=11, ha='center', va='center', color='darkred', fontweight='bold')
        
        # Arrow
        arrow = FancyArrowPatch((4.2, concern['y']), (5.8, concern['y']), 
                               arrowstyle='->', mutation_scale=25, 
                               linewidth=3, color='green')
        ax.add_patch(arrow)
        
        # Response (right)
        response_box = FancyBboxPatch((6, concern['y']-0.4), 3.5, 0.8, boxstyle="round,pad=0.1",
                                      edgecolor='green', facecolor='honeydew', linewidth=2)
        ax.add_patch(response_box)
        ax.text(7.75, concern['y'], concern['response'], 
                fontsize=9, ha='center', va='center', color='darkgreen', fontweight='bold')
        
        # Icon
        ax.text(5, concern['y'], concern['icon'], fontsize=20, ha='center')
    
    # Summary box
    summary_box = FancyBboxPatch((0.5, 0.1), 9, 0.8, boxstyle="round,pad=0.1",
                                 edgecolor='purple', facecolor='lavender', linewidth=3)
    ax.add_patch(summary_box)
    ax.text(5, 0.5, '💡 Kết luận: Prior là điểm MẠNH, không phải điểm YẾU của Bayesian Statistics!', 
            fontsize=12, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'addressing_subjectivity.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: addressing_subjectivity.png")

def create_chen_wins_debate(output_dir):
    """Image 7: Chen Wins the Debate"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Kết thúc Cuộc Tranh luận: Professor Chen Thắng!', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Stage
    stage = FancyBboxPatch((0.5, 4), 9, 4, boxstyle="round,pad=0.1", 
                           edgecolor='black', facecolor='lightblue', linewidth=2)
    ax.add_patch(stage)
    
    # Dr. Roberts (left) - thinking, uncertain
    roberts_head = Circle((2, 6.5), 0.4, facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(roberts_head)
    roberts_body = FancyBboxPatch((1.6, 5.2), 0.8, 1.3, boxstyle="round,pad=0.05",
                                  edgecolor='black', facecolor='coral', linewidth=2)
    ax.add_patch(roberts_body)
    
    # Roberts' eyes (uncertain)
    ax.plot(1.85, 6.55, 'ko', markersize=4)
    ax.plot(2.15, 6.55, 'ko', markersize=4)
    
    # Roberts' mouth (uncertain)
    ax.plot([1.85, 2.15], [6.35, 6.35], 'k-', linewidth=2)
    
    # Roberts' thought bubble
    thought = Circle((1.2, 7.5), 0.5, facecolor='white', edgecolor='gray', linewidth=2)
    ax.add_patch(thought)
    ax.text(1.2, 7.5, '🤔', fontsize=25, ha='center')
    ax.text(2, 4.8, 'Dr. Roberts\n(đang suy nghĩ...)', 
            fontsize=10, ha='center', style='italic')
    
    # Professor Chen (right) - confident, smiling
    chen_head = Circle((8, 6.5), 0.4, facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(chen_head)
    chen_body = FancyBboxPatch((7.6, 5.2), 0.8, 1.3, boxstyle="round,pad=0.05",
                               edgecolor='black', facecolor='mediumseagreen', linewidth=2)
    ax.add_patch(chen_body)
    
    # Chen's eyes (happy)
    ax.plot(7.85, 6.55, 'ko', markersize=5)
    ax.plot(8.15, 6.55, 'ko', markersize=5)
    
    # Chen's mouth (big smile)
    smile = patches.Arc((8, 6.35), 0.35, 0.25, angle=0, theta1=200, theta2=340, 
                       color='black', linewidth=2)
    ax.add_patch(smile)
    
    ax.text(8, 4.8, 'Professor Chen\n(tự tin!)', 
            fontsize=10, ha='center', fontweight='bold')
    
    # Chen's speech bubble with key points
    bubble = FancyBboxPatch((4.5, 5), 4.5, 2.5, boxstyle="round,pad=0.15",
                           edgecolor='green', facecolor='honeydew', linewidth=3)
    ax.add_patch(bubble)
    ax.text(6.75, 7.2, 'Chen\'s Kết luận:', fontsize=11, ha='center', fontweight='bold', color='darkgreen')
    ax.text(6.75, 6.8, '1. MINH BẠCH: Prior có thể kiểm tra', fontsize=9, ha='center')
    ax.text(6.75, 6.5, '2. KHÁCH QUAN: Dựa trên 10,000 BN', fontsize=9, ha='center')
    ax.text(6.75, 6.2, '3. DỮ LIỆU MẠNH: Sẽ áp đảo prior', fontsize=9, ha='center')
    ax.text(6.75, 5.9, '4. KIỂM TRA ĐƯỢC: Sensitivity analysis', fontsize=9, ha='center')
    ax.text(6.75, 5.5, '"Vậy, ai thực sự khách quan hơn?"', 
            fontsize=10, ha='center', style='italic', color='darkgreen', fontweight='bold')
    
    # Audience reaction
    ax.text(5, 3.5, '👏 👏 👏 👏 👏 👏 👏 👏', fontsize=25, ha='center')
    ax.text(5, 3, 'Khán giả vỗ tay!', fontsize=13, ha='center', fontweight='bold')
    
    # Winner badge
    winner_box = FancyBboxPatch((6.5, 8.2), 3, 1, boxstyle="round,pad=0.1",
                                edgecolor='gold', facecolor='lightyellow', linewidth=3)
    ax.add_patch(winner_box)
    ax.text(8, 8.7, '🏆 THẮNG!', fontsize=16, ha='center', fontweight='bold', color='gold')
    
    # Lesson learned
    lesson_box = FancyBboxPatch((0.5, 0.3), 9, 2.2, boxstyle="round,pad=0.15",
                                edgecolor='purple', facecolor='lavender', linewidth=3)
    ax.add_patch(lesson_box)
    ax.text(5, 2.2, '📚 Bài học:', fontsize=13, ha='center', fontweight='bold')
    ax.text(5, 1.8, 'Prior không phải là "chủ quan tùy tiện"', fontsize=11, ha='center')
    ax.text(5, 1.4, 'Prior là cách MINH BẠCH hóa kiến thức và giả định', fontsize=11, ha='center')
    ax.text(5, 1, 'Prior cho phép kết hợp thông tin từ nhiều nguồn một cách có nguyên tắc', fontsize=11, ha='center')
    ax.text(5, 0.6, '→ Đây là điểm MẠNH, không phải điểm YẾU!', 
            fontsize=12, ha='center', fontweight='bold', color='green')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chen_wins_debate.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: chen_wins_debate.png")

def main():
    """Generate all cartoon images for Bài 2.3"""
    print("\n" + "="*70)
    print("GENERATING CARTOON IMAGES FOR BÀI 2.3: PRIOR")
    print("="*70 + "\n")
    
    create_prior_debate_intro(output_dir)
    create_what_is_prior(output_dir)
    create_why_need_prior(output_dir)
    create_prior_types_spectrum(output_dir)
    create_combining_information(output_dir)
    create_addressing_subjectivity(output_dir)
    create_chen_wins_debate(output_dir)
    
    print("\n" + "="*70)
    print("✅ ALL 7 CARTOON IMAGES GENERATED SUCCESSFULLY!")
    print("="*70)
    print(f"\nImages saved to: {output_dir}")
    print("\nList of generated images:")
    print("  1. prior_debate_intro.png")
    print("  2. what_is_prior.png")
    print("  3. why_need_prior.png")
    print("  4. prior_types_spectrum.png")
    print("  5. combining_information.png")
    print("  6. addressing_subjectivity.png")
    print("  7. chen_wins_debate.png")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
