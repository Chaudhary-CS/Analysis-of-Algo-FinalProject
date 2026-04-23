"""
Export report.md to a clean HTML file, then save as PDF from your browser.

Run:
    python3 export_pdf.py

This opens report.html in your browser automatically.
Then: File > Print > Save as PDF  (or Cmd+P > Save as PDF on Mac)
"""

import markdown2
import os
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("report.md", "r") as f:
    md_text = f.read()

html_body = markdown2.markdown(
    md_text,
    extras=["tables", "fenced-code-blocks", "strike", "header-ids"]
)

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Graph Algorithms in Network Optimization - Tampa</title>
<style>
  @media print {{
    body {{ margin: 0; }}
    .no-print {{ display: none; }}
    img {{ max-width: 100%; page-break-inside: avoid; }}
    h2 {{ page-break-before: auto; }}
    pre {{ page-break-inside: avoid; }}
    table {{ page-break-inside: avoid; }}
  }}
  body {{
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11.5pt;
    line-height: 1.7;
    color: #1A202C;
    max-width: 860px;
    margin: 40px auto;
    padding: 0 40px 60px 40px;
  }}
  h1 {{
    font-size: 22pt;
    color: #1A365D;
    border-bottom: 3px solid #2B6CB0;
    padding-bottom: 8px;
    margin-top: 0;
  }}
  h2 {{
    font-size: 15pt;
    color: #2B6CB0;
    margin-top: 36px;
    margin-bottom: 10px;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 4px;
  }}
  h3 {{
    font-size: 12.5pt;
    color: #2D3748;
    margin-top: 22px;
    margin-bottom: 6px;
  }}
  h4 {{
    font-size: 11.5pt;
    font-weight: bold;
    color: #2D3748;
    margin-top: 16px;
  }}
  p {{ margin: 10px 0; }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
    font-size: 10.5pt;
  }}
  th {{
    background-color: #2B6CB0;
    color: white;
    padding: 8px 12px;
    text-align: left;
    font-weight: bold;
  }}
  td {{
    padding: 7px 12px;
    border-bottom: 1px solid #E2E8F0;
  }}
  tr:nth-child(even) td {{ background-color: #F7FAFC; }}
  code {{
    background: #EDF2F7;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 10pt;
  }}
  pre {{
    background: #F7FAFC;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #2B6CB0;
    padding: 14px 16px;
    border-radius: 4px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 9.5pt;
    line-height: 1.55;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
  }}
  pre code {{ background: none; padding: 0; font-size: inherit; }}
  img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto;
    border: 1px solid #CBD5E0;
    border-radius: 6px;
  }}
  em {{
    display: block;
    text-align: center;
    color: #4A5568;
    font-size: 10pt;
    margin-top: -12px;
    margin-bottom: 20px;
  }}
  strong {{ color: #1A202C; }}
  ul, ol {{ margin: 10px 0; padding-left: 26px; }}
  li {{ margin: 5px 0; }}
  hr {{ border: none; border-top: 1px solid #E2E8F0; margin: 28px 0; }}
  .print-hint {{
    background: #EBF8FF;
    border: 1px solid #BEE3F8;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 28px;
    font-family: -apple-system, sans-serif;
    font-size: 10pt;
    color: #2C5282;
  }}
</style>
</head>
<body>
<div class="print-hint no-print">
  <strong>To save as PDF:</strong> Press <strong>Cmd + P</strong> (Mac) or <strong>Ctrl + P</strong> (Windows),
  then choose <strong>Save as PDF</strong> as the destination. Set paper size to Letter and margins to Default.
  Uncheck "Headers and Footers" for a cleaner look.
</div>
{html_body}
</body>
</html>"""

with open("report.html", "w") as f:
    f.write(full_html)

print("Saved: report.html")
print("Opening in your browser — press Cmd+P then Save as PDF.")
subprocess.run(["open", "report.html"])
