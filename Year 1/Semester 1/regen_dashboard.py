#!/usr/bin/env python3
from pathlib import Path

src = Path("D:/Academic/Year 1/Semester 1/MSE_1st_Semester_Dashboard.html").read_text(encoding='utf-8')
out = Path("D:/Academic/Year 1/Semester 1/MSE_1st_Semester_Dashboard_new.html").write_text
# Just write it back unchanged for now; using terminal script instead
