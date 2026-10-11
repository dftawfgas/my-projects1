import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

# ---------- 中文字体 ----------
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei',
                                   'Noto Sans CJK SC', 'WenQuanYi Zen Hei',
                                   'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ================= 模型参数 =================
x0, smax, w, Hdec = 47.5, 4.0, 26.0, 28.0   # 沉降中心/最大下沉/槽宽/衰减深度
gx1, gx2 = 33.0, 62.0                        # 采空区左右边界
gy1, gy2 = -39.7, -34.3                      # 采空区顶底板

def gfun(y):
    """沉降随深度衰减系数"""
    return np.exp(-(np.maximum(-y, 0.0) / Hdec) ** 2)

def ydef(y0, x):
    """原始高程 y0 经沉降后的实际高程"""
    return y0 - smax * np.exp(-((np.asarray(x) - x0) / w) ** 2) * gfun(y0)

xs = np.linspace(0, 100, 1201)

# ================= 画布 =================
fig, ax = plt.subplots(figsize=(14, 8.6), dpi=110)
ax.set_xlim(-4, 104)
ax.set_ylim(-58, 9)
ax.axis('off')
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

# ================= 1. 岩层 =================
layers = [
    (  0,  -8, '#EADCB0', '第四系松散层'),
    ( -8, -18, '#D9BE93', '砂  岩'),
    (-18, -28, '#A9BFA6', '泥  岩'),
    (-28, -34, '#C9A97B', '砂  岩'),
    (-34, -40, '#4A4A4A', '煤  层'),
    (-40, -48, '#C6D0D8', '石灰岩'),
    (-48, -56, '#93A1AB', '基  底'),
]
for yt, yb, c, _ in layers:
    y1 = ydef(yt, xs)
    y2 = ydef(yb, xs)
    verts = np.vstack([np.column_stack([xs, y1]),
                       np.column_stack([xs[::-1], y2[::-1]])])
    ax.add_patch(Polygon(verts, closed=True, facecolor=c,
                         edgecolor='#707070', lw=0.8, zorder=2))

# 岩性标注
for yy, txt in [(-4, '第四系松散层'), (-13, '砂岩'), (-23, '泥岩'),
                (-31, '砂岩'), (-37, '煤层'), (-44, '石灰岩'), (-52, '基底')]:
    ax.text(3, yy, txt, fontsize=9, color='#4A4A4A',
            va='center', ha='left', zorder=6)

# ================= 2. 采空区（空洞） =================
ax.add_patch(Rectangle((gx1, gy1), gx2 - gx1, gy2 - gy1,
                       facecolor='#141414', edgecolor='#8A8A8A',
                       lw=1.0, zorder=3))

# 底部垮落矸石
rng = np.random.default_rng(2024)
for _ in range(220):
    cx = rng.uniform(gx1 + 0.4, gx2 - 0.4)
    cy = gy1 + (gy2 - gy1) * 0.62 * (rng.random() ** 1.6)
    r  = rng.uniform(0.30, 0.70)
    n  = rng.integers(4, 7)
    a  = np.linspace(0, 2 * np.pi, n, endpoint=False) + rng.uniform(0, 2 * np.pi)
    rr = r * rng.uniform(0.65, 1.3, n)
    v  = np.column_stack([cx + rr * np.cos(a), cy + rr * np.sin(a)])
    ax.add_patch(Polygon(v, closed=True, facecolor='#4E4E4E',
                         edgecolor='#707070', lw=0.4, zorder=4))

ax.text((gx1 + gx2) / 2, gy2 - 1.4, '采 空 区',
        fontsize=11, color='#FFFFFF', ha='center', va='center',
        fontweight='bold', zorder=8)

# ================= 3. 冒落带（破碎岩块） =================
ax.add_patch(Rectangle((gx1, -34.3), gx2 - gx1, 4.9,
                       facecolor='#8B7B68', edgecolor='none',
                       alpha=0.30, zorder=4))

for _ in range(280):
    cx = rng.uniform(gx1 + 0.5, gx2 - 0.5)
    cy = rng.uniform(-34.1, -29.6)
    r  = rng.uniform(0.45, 0.85)
    n  = rng.integers(4, 7)
    a  = np.linspace(0, 2 * np.pi, n, endpoint=False) + rng.uniform(0, 2 * np.pi)
    rr = r * rng.uniform(0.65, 1.3, n)
    v  = np.column_stack([cx + rr * np.cos(a), cy + rr * np.sin(a)])
    ax.add_patch(Polygon(v, closed=True, facecolor='#9C8B75',
                         edgecolor='#5E5346', lw=0.45, zorder=5))

# ================= 4. 裂隙带（竖向裂隙） =================
for _ in range(70):
    cx = rng.uniform(gx1 + 0.8, gx2 - 0.8)
    y1 = rng.uniform(-30.3, -25.0)
    y2 = y1 + rng.uniform(1.5, 5.0)
    yy = np.linspace(y1, y2, 16)
    xx = cx + 0.40 * np.sin(np.linspace(0, 3.5 * np.pi, 16) + rng.uniform(0, 6))
    ax.plot(xx, yy, color='#6B5B45', lw=rng.uniform(0.6, 1.2),
            alpha=0.85, zorder=5)

# 贯穿性大裂隙
for cx in [37.5, 44.0, 52.5, 58.0]:
    yy = np.linspace(-30.5, -21.5, 30)
    xx = cx + 0.7 * np.sin(np.linspace(0, 2.4 * np.pi, 30))
    ax.plot(xx, yy, color='#55483A', lw=1.6, alpha=0.9, zorder=5)

# ================= 5. 应力拱 =================
t = np.linspace(0, np.pi, 240)
ax.plot(x0 + 17.5 * np.cos(t), -34.3 + 21.0 * np.sin(t),
        ls=(0, (7, 5)), color='#D64541', lw=2.2, alpha=0.92, zorder=8)

ax.text(x0, -17.0, '应 力 拱', fontsize=11, color='#C0392B',
        ha='center', va='center', fontweight='bold', zorder=9,
        bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.85))

# 拱脚传力箭头
for (xa, ya, xb, yb) in [(34.0, -25.0, 30.0, -33.0),
                         (61.0, -25.0, 65.0, -33.0)]:
    ax.annotate('', xy=(xb, yb), xytext=(xa, ya),
                arrowprops=dict(arrowstyle='-|>', color='#D64541',
                                lw=2.0, mutation_scale=16), zorder=9)

# ================= 6. 应力集中 =================
for yc in (-35.5, -38.5):
    ax.annotate('', xy=(gx1 - 0.8, yc), xytext=(gx1 - 12, yc),
                arrowprops=dict(arrowstyle='-|>', color='#D64541',
                                lw=2.2, mutation_scale=17), zorder=9)
ax.text(gx1 - 13, -32.6, '应力集中', fontsize=10.5, color='#C0392B',
        ha='center', va='center', fontweight='bold', zorder=9,
        bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.85))

# ================= 7. 应力向深部转移 =================
for xa in (35.0, 47.5, 60.0):
    ax.annotate('', xy=(xa, -50.5), xytext=(xa, -42.0),
                arrowprops=dict(arrowstyle='-|>', color='#E67E22',
                                lw=2.2, mutation_scale=17), zorder=9)
ax.text(68, -46.5, '应力向深部转移', fontsize=10.5, color='#CA6F1E',
        ha='left', va='center', fontweight='bold', zorder=9,
        bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.85))

# ================= 8. 覆岩弯曲下沉箭头 =================
for xa in (40.0, 47.5, 55.0):
    ax.annotate('', xy=(xa, -22.0), xytext=(xa, -14.5),
                arrowprops=dict(arrowstyle='-|>', color='#1F6FB2',
                                lw=1.8, mutation_scale=14, alpha=0.85), zorder=9)

# ================= 9. 三带标注括号 =================
def draw_brace(x, y_top, y_bot, label, color):
    ax.plot([x, x], [y_bot, y_top], color=color, lw=1.8, zorder=10)
    ax.plot([x, x + 1.3], [y_top, y_top], color=color, lw=1.8, zorder=10)
    ax.plot([x, x + 1.3], [y_bot, y_bot], color=color, lw=1.8, zorder=10)
    ax.text(x + 2.4, (y_top + y_bot) / 2, label, fontsize=11.5,
            color=color, va='center', ha='left',
            fontweight='bold', zorder=10)

draw_brace(66.0, -34.3, -29.5, '冒落带', '#C0392B')
draw_brace(66.0, -29.5, -21.0, '裂隙带', '#D68910')
draw_brace(66.0, -21.0,  -1.5, '弯曲下沉带', '#2471A3')

# ================= 10. 地表沉降 =================
ysurf = ydef(0, xs)

# 原始地表参考线
ax.plot([0, 100], [0, 0], ls='--', color='#8A8A8A', lw=1.2, zorder=10)

# 沉降盆地填充
ax.fill_between(xs, ysurf, 0, color='#2E7D32', alpha=0.18, zorder=1)

# 沉降后地表曲线
ax.plot(xs, ysurf, color='#2E7D32', lw=3.2, zorder=11,
        solid_capstyle='round')

# 最大下沉标注
ax.annotate('', xy=(x0, ydef(0, x0)), xytext=(x0, 0),
            arrowprops=dict(arrowstyle='<|-|>', color='#333333',
                            lw=1.6, mutation_scale=14), zorder=12)
ax.text(x0 + 1.8, ydef(0, x0) / 2, '最大下沉 W₀', fontsize=10,
        color='#333333', va='center', ha='left', zorder=12,
        bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85))

# 标题
ax.text(x0, 6.0, '地下开挖引起的覆岩破坏与地表沉降示意图',
        fontsize=16, ha='center', va='center',
        fontweight='bold', color='#1A1A1A', zorder=15)

# 地表沉降文字
ax.text(x0 - 26, 3.2, '地表沉降盆地', fontsize=11.5, color='#2E7D32',
        ha='center', va='center', fontweight='bold', zorder=12,
        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#2E7D32',
                  lw=1.0, alpha=0.9))
ax.annotate('', xy=(x0 - 20, -0.6), xytext=(x0 - 23, 1.6),
            arrowprops=dict(arrowstyle='-|>', color='#2E7D32',
                            lw=1.6, mutation_scale=14), zorder=12)

plt.savefig('地下开挖覆岩破坏与地表沉降示意图.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.show()