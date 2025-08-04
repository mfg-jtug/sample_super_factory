#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""Tableau リポジトリ追加リソース インストーラ（結果明示版）"""

import sys, time, shutil, stat, zipfile, base64, ctypes, tkinter as tk
from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox

# DPI
try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception: pass

def R(rel:str)->Path: return Path(getattr(sys,"_MEIPASS",Path(__file__).parent),rel)

# ─── 共通ヘルパ ──────────────────────────────────────────
def backup(p:Path):
    if p.exists():
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(p, p.with_name(f"{p.stem}_{ts}{p.suffix}"))

def rm_rf(path:Path):
    def _onerr(func,pth,_):
        try: Path(pth).chmod(Path(pth).stat().st_mode|stat.S_IWRITE)
        except Exception: pass
        func(pth)
    shutil.rmtree(path,onerror=_onerr)

def cp_retry(src:Path,dst:Path,actions:list[str]):
    for _ in range(3):
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src,dst)
            actions.append(f"{src.name} → {dst.relative_to(dst.parents[2])}")
            return
        except PermissionError: time.sleep(1)
    raise

# ─── リポジトリ検出（標準＋日本語＋レジストリ） ─────────────────────
def guess_repo()->Path|None:
    doc=Path.home()/ "Documents"
    for name in ("My Tableau Repository","マイ Tableau リポジトリ"):
        p=doc/name
        if p.exists(): return p
    if sys.platform=="win32":
        import winreg,re
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"SOFTWARE\Tableau") as rt:
                latest=sorted(k for k in (winreg.EnumKey(rt,i)
                    for i in range(winreg.QueryInfoKey(rt)[0]))
                    if k.startswith("Tableau "))[-1]
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                fr"SOFTWARE\Tableau\{latest}\Settings") as k:
                for i in range(winreg.QueryInfoKey(k)[1]):
                    n,v,_=winreg.EnumValue(k,i)
                    if re.fullmatch(r"RepositoryLocation(\d+)?",n):
                        p=Path(v).expanduser()
                        if p.exists(): return p
        except FileNotFoundError: pass
    return None

# ─── Shapes 展開 ─────────────────────────────────────────────
def deploy_shapes(root:Path,errs:list[str],actions:list[str]):
    root.mkdir(parents=True, exist_ok=True)
    tmp=root/"_shapes_tmp"; tmp.exists() and rm_rf(tmp)
    zipfile.ZipFile(R("Shape.zip")).extractall(tmp)
    for src in [p for p in tmp.iterdir() if p.is_dir()]:
        dst=root/src.name
        if dst.exists():
            try: backup(dst); rm_rf(dst)
            except PermissionError: pass
        try: src.rename(dst); actions.append(f"{src.name}/ → {dst.relative_to(root.parent)}")
        except Exception:
            for f in src.rglob("*"):
                d=dst/f.relative_to(src)
                try:
                    d.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copy2(f,d) if f.is_file() else d.mkdir(exist_ok=True)
                except PermissionError: errs.append(str(d))
            rm_rf(src)
    rm_rf(tmp)

# ─── インストール処理 ───────────────────────────────────────
def install(repo:Path)->tuple[list[str],list[str]]:
    errs: list[str]=[]
    actions:list[str]=[]

    try: cp_retry(R("Preferences.tps"), repo/"Preferences.tps", actions)
    except Exception as e: errs.append(f"Preferences.tps → {e}")

    themes=repo/"Themes"; themes.mkdir(parents=True, exist_ok=True)
    try: cp_retry(R("ssf_curry.json"), themes/"ssf_curry.json", actions)
    except Exception as e: errs.append(f"ssf_curry.json → {e}")

    for ds in (repo/"Datasources", repo/"データソース", repo/"データ ソース"):
        if ds==repo/"Datasources" or ds.exists():
            try: cp_retry(R("サンプルスーパーファクトリー.xlsx"),
                          ds/"サンプルスーパーファクトリー.xlsx", actions)
            except Exception as e: errs.append(f"{ds} → {e}")

    deploy_shapes(repo/"Shapes", errs, actions)
    jp=repo/"形状"
    if jp.exists():
        deploy_shapes(jp, errs, actions)

    return errs, actions

# ─── GUI（rootのみ）──────────────────────────────────────────
def ask_repo()->Path|None:
    root=tk.Tk(); root.title("インストール先の確認"); root.attributes('-topmost',True)
    root.resizable(False,False)
    sel=tk.StringVar(value=str(guess_repo() or "未検出"))

    # 画像 or テキスト
    try:
        img=tk.PhotoImage(data=base64.b64encode(R("ssx.png").read_bytes()).decode())
        tk.Label(root,image=img).pack()
    except Exception:
        tk.Label(root,text="Sample Super XXX",font=("Segoe UI",16)).pack(pady=30)

    tk.Label(root,text="インストール先フォルダ:",anchor="w")\
        .pack(fill="x",padx=12)
    tk.Label(root,textvariable=sel,relief="sunken",anchor="w")\
        .pack(fill="x",padx=12,pady=4)

    def browse():
        p=filedialog.askdirectory(initialdir=str(Path.home()),title="リポジトリフォルダを選択")
        if p: sel.set(p); ok.config(state="normal",default="active")

    def accept(): root.quit()
    def cancel(): sel.set(""); root.quit()

    btn=tk.Frame(root); btn.pack(pady=10)
    ok=tk.Button(btn,text="OK",width=10,command=accept,
                default="active" if sel.get()!="未検出" else "disabled",
                state="normal"  if sel.get()!="未検出" else "disabled")
    ok.grid(row=0,column=0,padx=5)

    browse_btn=tk.Button(btn,text="別フォルダ...",width=10,command=browse)
    browse_btn.grid(row=0,column=1,padx=5); browse_btn.focus_set()

    tk.Button(btn,text="キャンセル",width=10,command=cancel)\
      .grid(row=0,column=2,padx=5)

    # サイズ確定→中央
    root.update_idletasks()
    w=540; h=root.winfo_reqheight()
    x=root.winfo_screenwidth()//2-w//2; y=root.winfo_screenheight()//2-h//2
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop(); root.destroy()
    return Path(sel.get()) if sel.get() and sel.get()!="未検出" else None

# ─── Main ────────────────────────────────────────────────
def main():
    repo=ask_repo()
    if not repo: return
    errs,actions=install(repo)

    details="\n".join(f"・{a}" for a in actions) if actions else "（ファイルコピーなし）"
    if errs:
        messagebox.showwarning("Installer (警告あり)",
            f"{repo}\nにインストールしましたが、以下で問題がありました:\n\n"+"\n".join(errs))
    else:
        messagebox.showinfo("Installer 完了",
            f"インストール先: {repo}\n\nコピーした項目:\n{details}")

if __name__=="__main__":
    try: main()
    except Exception as exc:
        import traceback,tempfile
        Path(tempfile.gettempdir(),"ssx_installer_error.log")\
            .write_text("".join(traceback.format_exc()))
        tk.Tk().withdraw(); messagebox.showerror("Installer – 予期せぬエラー",str(exc))
