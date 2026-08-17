"""
DOI 批量核对（Crossref API）。
用法: python code/common/verify_dois.py --file related_work/dois_to_verify.json
输出: related_work/doi_verify_report.md
"""
import argparse
import json
import os
import time
import urllib.request

CROSSREF = "https://api.crossref.org/works/{}"


def fetch_doi(doi, retries=3):
    url = CROSSREF + urllib.parse.quote(doi)
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AdvFake-project/1.0 (mailto:test@example.com)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)["message"]
        except Exception as e:
            if i == retries - 1:
                return {"error": str(e)}
            time.sleep(3 * (i + 1))


def main():
    import urllib.parse
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=os.path.join(os.path.dirname(__file__), "..", "..", "related_work", "dois_to_verify.json"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "..", "related_work", "doi_verify_report.md"))
    args = ap.parse_args()

    with open(args.file) as f:
        items = json.load(f)

    lines = ["# DOI 核对报告", "", "| # | 记录条目 | DOI | Crossref 状态 | 标题匹配 | 年 | 期刊 |", "|---|---|---|---|---|---|---|"]
    for it in items:
        doi = it.get("doi")
        rec = it.get("title", "")
        if not doi or not doi.startswith("10."):
            lines.append(f"| {it.get('id')} | {rec} | {doi or 'N/A'} | ⚠️ 无有效 DOI | - | - | - |")
            continue
        msg = fetch_doi(doi)
        if "error" in msg:
            lines.append(f"| {it.get('id')} | {rec} | {doi} | ❌ {msg['error'][:60]} | - | - | - |")
        else:
            title = (msg.get("title") or [""])[0]
            year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
            cont = (msg.get("container-title") or [""])[0]
            match = "✅" if rec.lower() in title.lower() or title.lower() in rec.lower() else "❌"
            lines.append(f"| {it.get('id')} | {rec} | {doi} | ✅ | {match} | {year} | {cont[:40]} |")
        time.sleep(1.2)  # 限速

    with open(args.out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"report -> {args.out}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
