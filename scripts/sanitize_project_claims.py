from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "project_media_records.json"

COPY = {
    "en": {
        "meta": "PROJECT MEDIA RECORD",
        "status_h": "Record status",
        "status": "This project record is supported by archived video and installation images. The public title and date follow the archived media filename.",
        "scope_h": "Documented scope",
        "scope": "The available media documents installed furniture and its spatial context. Exact product models, quantities, custom specifications and contractual scope remain pending source verification.",
        "policy_h": "Publication standard",
        "policy": "Client quotations and measured business or performance outcomes are not published unless they can be traced to approved project documents.",
    },
    "tw": {
        "meta": "專案媒體紀錄",
        "status_h": "紀錄狀態",
        "status": "本專案目前具有典藏影片與安裝圖片。公開名稱與日期依媒體檔名記錄，不延伸推測客戶承諾或專案成果。",
        "scope_h": "已記錄範圍",
        "scope": "現有媒體可確認家具安裝畫面與空間情境；確切產品型號、數量、客製規格及合約工作範圍仍待來源文件核對。",
        "policy_h": "發布標準",
        "policy": "未能追溯至核准專案文件的客戶引言、營運成效與性能結果，暫不公開。",
    },
    "jp": {
        "meta": "プロジェクト記録",
        "status_h": "記録状況",
        "status": "本記録には保管済みの動画と設置写真があります。公開する名称と日付はメディアファイル名に基づき、確認できない成果や顧客評価は追加していません。",
        "scope_h": "記録済み範囲",
        "scope": "現時点のメディアから、家具の設置状況と空間の文脈を確認できます。製品型番、数量、特注仕様、契約上の対応範囲は資料確認後に公開します。",
        "policy_h": "公開基準",
        "policy": "承認済みプロジェクト資料に遡れない顧客コメント、事業成果、性能結果は公開しません。",
    },
}


def narrative(copy: dict[str, str], video: str) -> str:
    return f'''<div class="uc-narrative scroll-reveal" style="transition-delay: 0.15s;">
          <div class="uc-text-block">
            <h4>{html.escape(copy['status_h'])}</h4>
            <p>{html.escape(copy['status'])}</p>
          </div>
          <div class="uc-text-block">
            <h4>{html.escape(copy['scope_h'])}</h4>
            <p>{html.escape(copy['scope'])}</p>
          </div>
          <div class="uc-text-block">
            <h4>{html.escape(copy['policy_h'])}</h4>
            <p>{html.escape(copy['policy'])}</p>
          </div>
          <p class="project-source-file">Source media: <code>{html.escape(video)}</code></p>
        </div>'''


def replace_section(content: str, record: dict, lang: str) -> str:
    section_pattern = re.compile(
        rf'(<section class="ultimate-case-section" id="{re.escape(record["id"])}".*?</section>)',
        re.DOTALL,
    )
    match = section_pattern.search(content)
    if not match:
        raise RuntimeError(f"Missing section {record['id']} in {lang}/projects.html")
    section = match.group(1)
    copy = COPY[lang]
    section = re.sub(
        r'(<div class="ultimate-case-header scroll-reveal">\s*<span class="meta">).*?(</span>\s*<h2>).*?(</h2>)',
        rf'\g<1>{html.escape(copy["meta"])} · {record["date"]}\g<2>{html.escape(record["titles"][lang])}\g<3>',
        section,
        count=1,
        flags=re.DOTALL,
    )
    start = section.find('<div class="uc-narrative')
    end_marker = "\n        </div>\n        \n      </div>"
    end = section.find(end_marker, start)
    if start < 0 or end < 0:
        raise RuntimeError(f"Missing narrative boundaries for {record['id']} in {lang}")
    section = section[:start] + narrative(copy, record["video"]) + section[end + len("\n        </div>"):]
    return content[:match.start()] + section + content[match.end():]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    for lang in COPY:
        path = ROOT / lang / "projects.html"
        content = path.read_text(encoding="utf-8")
        content = content.replace("</div>>", "</div>")
        for record in source["records"]:
            content = replace_section(content, record, lang)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"Sanitized {len(source['records']) * len(COPY)} localized project records.")


if __name__ == "__main__":
    main()
