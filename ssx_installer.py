#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ssx_installer.py – Tableau Repository Resource Installer
macOS / Windows 共通
"""

import sys, shutil, stat, zipfile, base64, tkinter as tk, os, unicodedata
from pathlib import Path
from tkinter import filedialog, messagebox

# ── DPI (Windows) ──────────────────────────────────────────
if sys.platform.startswith("win"):
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

# ── PyInstaller / ソース両対応でリソース取得 ───────────────
def R(rel: str) -> Path:
    """Bundle内（_MEIPASS）/ ソース同梱 のどちらでも動くリソース解決。"""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return base / rel  # PyInstaller 4.3+ では __file__ も絶対パスになる。参照: docs

# ── 汎用ヘルパ ─────────────────────────────────────────────
def cp(src: Path, dst: Path, log: list[str], *, base: Path, meta: bool = True):
    """
    meta=False → shutil.copy  (Windows errno 2 回避)
    meta=True  → shutil.copy2 (メタデータもコピー)
    base       → repo 直下を基準に相対パスを記録
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    (shutil.copy2 if meta else shutil.copy)(src, dst)
    log.append(f"{src.name} → {dst.relative_to(base)}")

def rm_dir(p: Path):
    def onerr(func, pth, _):
        try:
            Path(pth).chmod(Path(pth).stat().st_mode | stat.S_IWRITE)
        except Exception:
            pass
        func(pth)
    shutil.rmtree(p, onerror=onerr)

# ── Repository 自動検出 ───────────────────────────────────
def guess_repo() -> Path | None:
    """“My Tableau Repository / マイ Tableau リポジトリ” を優先検出。"""
    doc = Path.home() / "Documents"
    for n in ("My Tableau Repository", "マイ Tableau リポジトリ"):
        p = doc / n
        if p.exists():
            return p
    # （Windowsレジストリ探索は省略・必要なら後で戻す）
    return None

def pick_datasources_dir(repo: Path) -> Path:
    """
    Datasources の日本語ゆれ対策：
    - 既存のいずれかを優先採用（Datasources / データソース / データ ソース）
    - どれも無ければ 'Datasources' を作る
    Tableau 公式も My Documents 配下に My Tableau Repository が作られ、
    関連フォルダ（データ ソース等）に保存できる想定。 参照: help docs
    """
    candidates = ["Datasources", "データソース", "データ ソース"]
    for name in candidates:
        p = repo / name
        if p.is_dir():
            return p
    p = repo / "Datasources"
    p.mkdir(parents=True, exist_ok=True)
    return p

# ── Shapes 解凍 ───────────────────────────────────────────
def deploy_shapes(root: Path, log: list[str], errs: list[str], *, base: Path):
    tmp = root.parent / "_tmp_shapes"
    tmp.exists() and rm_dir(tmp)
    zipfile.ZipFile(R("Shape.zip")).extractall(tmp)
    for src in tmp.iterdir():
        dst = root / src.name
        if dst.exists():
            rm_dir(dst)
        try:
            src.rename(dst)
            log.append(f"{src.name}/ → {dst.relative_to(base)}")
        except Exception as e:
            errs.append(f"{src.name}: {e}")
    rm_dir(tmp)

# ── インストール処理 ─────────────────────────────────────
def install(repo: Path) -> tuple[list[str], list[str]]:
    # 念のため NFC 正規化（見た目同じ文字差を吸収）
    repo = Path(unicodedata.normalize("NFC", str(repo)))
    repo.mkdir(parents=True, exist_ok=True)

    log:  list[str] = []
    errs: list[str] = []

    def safe_cp(src: Path, dst: Path, label: str, *, meta: bool = True):
        try:
            cp(src, dst, log, base=repo, meta=meta)
        except OSError as e:
            errs.append(f"{label}: {e.strerror or e}")
        except Exception as e:
            errs.append(f"{label}: {e}")

    # 1) Preferences（メタなしコピー推奨）
    safe_cp(R("Preferences.tps"), repo / "Preferences.tps",
            "Preferences.tps", meta=False)

    # 2) Themes（json）
    themes = repo / "Themes"
    safe_cp(R("ssf_curry.json"), themes / "ssf_curry.json", "Themes/ssf_curry.json")

    # 3) Datasources（Excel 4ファイル）
    ds_dir = pick_datasources_dir(repo)
    excel_names = [
        "サンプルスーパーファクトリー_生産管理.xlsx",
        "サンプルスーパーファクトリー_製造技術.xlsx",
        "サンプルスーパーファクトリー_品質管理.xlsx",
        "サンプルスーパーファクトリー_製品マスタ.xlsx",
    ]
    for name in excel_names:
        safe_cp(R(name), ds_dir / name, f"{ds_dir.name}/{name}")

    # 4) 注意事項 PDF（リポジトリ直下）
    pdf_name = "利用上の注意点.pdf"
    safe_cp(R(pdf_name), repo / pdf_name, pdf_name)

    # 5) Shapes（英/日 どちらの“Shapes/形状”にも展開）
    shapes_root = repo / "Shapes"
    deploy_shapes(shapes_root, log, errs, base=repo)
    jp = repo / "形状"
    if jp.exists():
        deploy_shapes(jp, log, errs, base=repo)

    return log, errs

# ── GUI ──────────────────────────────────────────────────
def ask_repo() -> Path | None:
    root = tk.Tk()
    root.title("インストール先を選択")
    root.attributes("-topmost", True)
    sel = tk.StringVar(value=str(guess_repo() or "未検出"))

    try:
        img = tk.PhotoImage(data=base64.b64encode(R("ssx.png").read_bytes()).decode())
        tk.Label(root, image=img).pack()
    except Exception:
        tk.Label(root, text="Sample Super XXX", font=("Helvetica", 16)).pack(pady=30)

    tk.Label(root, text="インストール先フォルダ:", anchor="w").pack(fill="x", padx=12)
    tk.Label(root, textvariable=sel, relief="sunken", anchor="w").pack(fill="x", padx=12, pady=4)

    def browse():
        p = filedialog.askdirectory(title="Repository フォルダを選択")
        if p:
            sel.set(p)

    tk.Button(root, text="別フォルダ...", command=browse).pack(pady=4)
    tk.Button(root, text="OK", width=10, command=root.quit).pack(pady=6)

    root.mainloop()
    root.destroy()
    return Path(sel.get()) if sel.get() and sel.get() != "未検出" else None

# ── Main ────────────────────────────────────────────────
def main():
    repo = ask_repo()
    if not repo:
        return
    log, errs = install(repo)
    if errs:
        messagebox.showwarning("警告あり",
            f"{repo}\nへコピー中に問題:\n\n" + "\n".join(errs))
    messagebox.showinfo("完了",
        f"インストール先: {repo}\n\nコピーした項目:\n" + "\n".join(f"・{l}" for l in log))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback, tempfile
        Path(tempfile.gettempdir(), "ssx_installer_error.log").write_text("".join(traceback.format_exc()))
        tk.Tk().withdraw()
        messagebox.showerror("エラー", os.strerror(e.errno) if getattr(e, "errno", None) else str(e))
