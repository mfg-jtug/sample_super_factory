#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ssx_installer.py – Tableau Repository Resource Installer
macOS / Windows 共通（Windows は copy2→copy で errno 2 回避）
"""

import sys, time, shutil, stat, zipfile, base64, tkinter as tk, os
from pathlib import Path
from datetime import datetime
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
    return Path(getattr(sys, "_MEIPASS", Path(__file__).parent), rel)

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
    doc = Path.home() / "Documents"
    for n in ("My Tableau Repository", "マイ Tableau リポジトリ"):
        p = doc / n
        if p.exists():
            return p
    if sys.platform.startswith("win"):
        import winreg, re
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Tableau") as h:
                latest = sorted(k for k in (winreg.EnumKey(h, i)
                           for i in range(winreg.QueryInfoKey(h)[0]))
                           if k.startswith("Tableau "))[-1]
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                fr"SOFTWARE\Tableau\{latest}\Settings") as s:
                for i in range(winreg.QueryInfoKey(s)[1]):
                    n, v, _ = winreg.EnumValue(s, i)
                    if re.fullmatch(r"RepositoryLocation(\d+)?", n):
                        p = Path(v).expanduser()
                        if p.exists():
                            return p
        except FileNotFoundError:
            pass
    return None

# ── Shapes 解凍 ───────────────────────────────────────────
def deploy_shapes(root: Path, log: list[str], errs: list[str], *, base: Path):
    tmp = root / "_tmp_shapes"
    tmp.exists() and rm_dir(tmp)
    zipfile.ZipFile(R("Shape.zip")).extractall(tmp)
    for src in tmp.iterdir():
        dst = root / src.name
        if dst.exists():
            rm_dir(dst)
        try:
            src.rename(dst)
            log.append(f"{src.name}/ → {(dst).relative_to(base)}")
        except Exception as e:
            errs.append(f"{src} → {e}")
    rm_dir(tmp)

# ── インストール処理 ─────────────────────────────────────
def install(repo: Path) -> tuple[list[str], list[str]]:
    repo.mkdir(parents=True, exist_ok=True)           # ルート生成
    log:  list[str] = []
    errs: list[str] = []

    def safe_cp(src: Path, dst: Path, label: str, *, meta: bool = True):
        try:
            cp(src, dst, log, base=repo, meta=meta)
        except OSError as e:
            errs.append(f"{label}: {e.strerror or e}")

    # Preferences.tps は meta=False で errno 2 回避
    safe_cp(R("Preferences.tps"), repo / "Preferences.tps",
            "Preferences.tps", meta=False)

    themes = repo / "Themes"
    safe_cp(R("ssf_curry.json"), themes / "ssf_curry.json", "ssf_curry.json")

    for ds_name in ("Datasources", "データソース", "データ ソース"):
        ds = repo / ds_name
        if ds_name == "Datasources" or ds.exists():
            safe_cp(R("サンプルスーパーファクトリー.xlsx"),
                    ds / "サンプルスーパーファクトリー.xlsx", ds_name)

    deploy_shapes(repo / "Shapes", log, errs, base=repo)
    jp = repo / "形状"
    if jp.exists():
        deploy_shapes(jp, log, errs, base=repo)

    return log, errs

# ── GUI ──────────────────────────────────────────────────
def ask_repo() -> Path | None:
    root = tk.Tk()
    root.title("インストール先を選択")
    root.attributes('-topmost', True)
    sel = tk.StringVar(value=str(guess_repo() or "未検出"))

    try:
        img = tk.PhotoImage(data=base64.b64encode(R("ssx.png").read_bytes()).decode())
        tk.Label(root, image=img).pack()
    except Exception:
        tk.Label(root, text="Sample Super XXX", font=("Helvetica", 16)).pack(pady=30)

    tk.Label(root, text="インストール先フォルダ:", anchor="w")\
        .pack(fill="x", padx=12)
    tk.Label(root, textvariable=sel, relief="sunken", anchor="w")\
        .pack(fill="x", padx=12, pady=4)

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
        f"インストール先: {repo}\n\nコピーした項目:\n" +
        "\n".join(f"・{l}" for l in log))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback, tempfile
        Path(tempfile.gettempdir(), "ssx_installer_error.log")\
            .write_text("".join(traceback.format_exc()))
        tk.Tk().withdraw()
        messagebox.showerror("エラー", os.strerror(e.errno) if getattr(e, "errno", None) else str(e))
