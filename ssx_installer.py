#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ssx_installer.py  –  Shapes.zip の複数業種フォルダを展開し、
Excel を Datasources / データソース / データ ソース に配置。
GUI が出ない環境では CLI 入力にフォールバックします。
"""
import sys, time, shutil, stat, zipfile, base64, ctypes, tkinter as tk
from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox

# ── DPI ─────────────────────────────────────────────────────────
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

def R(rel: str) -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).parent), rel)

def backup(p: Path):
    if p.exists():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(p, p.with_name(f"{p.stem}_{ts}{p.suffix}"))

def writable_all(tree: Path):
    for p in tree.rglob("*"):
        try: p.chmod(p.stat().st_mode | stat.S_IWRITE)
        except PermissionError: pass

def rm_rf(path: Path):
    def onerr(f, p, _):
        Path(p).chmod(Path(p).stat().st_mode | stat.S_IWRITE); f(p)
    shutil.rmtree(path, onerror=onerr)

def cp_retry(src: Path, dst: Path):
    for _ in range(3):
        try: shutil.copy2(src, dst); return
        except PermissionError: time.sleep(1)
    raise

# ── Tableau Repo autodetect ────────────────────────────────────
def guess_repo() -> Path | None:
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Tableau") as rt:
            latest = sorted(k for k in (winreg.EnumKey(rt, i)
                for i in range(winreg.QueryInfoKey(rt)[0])) if k.startswith("Tableau "))[-1]
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            fr"SOFTWARE\Tableau\{latest}\Settings") as k:
            p = Path(winreg.QueryValueEx(k, "RepositoryLocation8")[0]).expanduser()
            if p.exists(): return p
    except Exception: pass
    dflt = Path.home()/"Documents"/"My Tableau Repository"
    return dflt if dflt.exists() else None

# ── Shapes 展開 (複数フォルダ) ────────────────────────────────
def deploy_all_shapes(shapes_root: Path, errs: list[str]):
    shapes_root.mkdir(parents=True, exist_ok=True)
    tmp = shapes_root / "_shapes_tmp"
    if tmp.exists(): rm_rf(tmp)
    zipfile.ZipFile(R("Shape.zip")).extractall(tmp)

    for src_dir in [p for p in tmp.iterdir() if p.is_dir()]:
        dst_dir = shapes_root / src_dir.name
        if dst_dir.exists():
            try: backup(dst_dir); rm_rf(dst_dir)
            except PermissionError: pass        # 警告に乗せない
        try: src_dir.rename(dst_dir)
        except (PermissionError, FileExistsError):
            for p in src_dir.rglob("*"):
                d = dst_dir / p.relative_to(src_dir)
                try:
                    d.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, d) if p.is_file() else d.mkdir(exist_ok=True)
                except PermissionError: errs.append(str(d))
            rm_rf(src_dir)
        writable_all(dst_dir)
    rm_rf(tmp)

# ── Installer 本体 ────────────────────────────────────────────
def install(repo: Path) -> list[str]:
    errs=[]
    try: cp_retry(R("Preferences.tps"), repo/"Preferences.tps")
    except Exception as e: errs.append(f"Preferences.tps → {e}")

    themes = repo/"Themes"; themes.mkdir(parents=True, exist_ok=True)
    try: cp_retry(R("ssf_curry.json"), themes/"ssf_curry.json")
    except Exception as e: errs.append(f"ssf_curry.json → {e}")

    for ds in (repo/"Datasources",
               repo/"データソース",
               repo/"データ ソース"):             # ★ スペースありも追加
        if ds == repo/"Datasources" or ds.exists():
            ds.mkdir(parents=True, exist_ok=True)
            try:
                cp_retry(R("サンプルスーパーファクトリー.xlsx"),
                         ds/"サンプルスーパーファクトリー.xlsx")
            except Exception as e: errs.append(f"{ds} → {e}")

    deploy_all_shapes(repo/"Shapes", errs)
    if (repo/"形状").exists():
        deploy_all_shapes(repo/"形状", errs)
    return errs

# ── Splash ─────────────────────────────────────────────────────
def splash(root: tk.Tk):
    top = tk.Toplevel(root); top.title("Sample Super xxx")
    img = tk.PhotoImage(data=base64.b64encode(R("ssx.png").read_bytes()))
    top.geometry(f"{img.width()}x{img.height()+80}")
    top.resizable(False, False); top.attributes('-topmost', True)
    cv=tk.Canvas(top,width=img.width(),height=img.height(),highlightthickness=0)
    cv.pack(); cv.create_image(0,0,anchor="nw",image=img)
    tk.Label(top,text="サンプルスーパーxxx をインストールします。\n"
                      "OK 後 Tableau リポジトリを選択してください。",
             font=("Segoe UI",11)).pack(pady=10)
    tk.Button(top,text="OK",width=10,command=top.destroy).pack(pady=2)
    top.transient(root); top.grab_set(); root.wait_window(top)

# ── Repo select GUI→CLI fallback ───────────────────────────────
def select_repo(root: tk.Tk, initial: Path) -> Path|None:
    root.lift(); root.attributes('-topmost',True); root.update()
    folder=filedialog.askdirectory(parent=root,
            initialdir=str(initial),
            title="Tableau リポジトリフォルダを選択してください")
    root.attributes('-topmost',False)
    if folder: return Path(folder)
    print("\nダイアログが表示されませんでした。")
    while True:
        p=Path(input("リポジトリのパス（空で中止）> ").strip('"')).expanduser()
        if not p: return None
        if p.exists(): return p
        print("存在しません。再入力を。")

# ── Entry ──────────────────────────────────────────────────────
def main():
    root=tk.Tk(); root.geometry("1x1+100+100"); root.overrideredirect(True)
    splash(root)
    repo=select_repo(root, guess_repo() or Path.home()/"Documents")
    root.destroy()
    if not repo: print("キャンセル"); return
    issues=install(repo)
    if issues:
        messagebox.showwarning("Installer (警告あり)",
                               "完了しましたが問題:\n\n"+"\n".join(issues))
    else:
        messagebox.showinfo("Installer","インストール完了！")

if __name__=="__main__":
    try: main()
    except Exception as exc:
        import traceback,tempfile
        log=Path(tempfile.gettempdir())/"ssx_installer_error.log"
        log.write_text("".join(traceback.format_exc()))
        tk.Tk().withdraw()
        messagebox.showerror("Installer – 予期せぬエラー",
            f"{exc.__class__.__name__}: {exc}\n\n詳細ログ: {log}")
