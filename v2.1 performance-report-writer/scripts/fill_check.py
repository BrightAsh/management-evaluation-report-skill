#!/usr/bin/env python3
# 사용법: python3 fill_check.py 변환된.pdf  → 쪽별 내용 하단 비율 (0.95 넘으면 위험, 0.80~0.90 권장)
import sys, subprocess, glob, os, tempfile
import numpy as np
from PIL import Image
d = tempfile.mkdtemp(); subprocess.run(['pdftoppm', '-r', '60', '-png', sys.argv[1], d + '/p'], check=True)
for f in sorted(glob.glob(d + '/p-*.png')):
    a = np.array(Image.open(f).convert('L')); h = a.shape[0]
    rows = np.where((a[:int(h * 0.94)] < 200).sum(1) > 3)[0]
    print(os.path.basename(f), round(rows.max() / h, 3) if len(rows) else 0)
