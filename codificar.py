#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import base64
import random
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# ================= CIFRADO CÉSAR =====================

ALFABETO = "abcdefghijklmnñopqrstuvwxyz"
ALFABETO_M = ALFABETO.upper()
alphabet_len = len(ALFABETO)

# Rotor wirings
rotor_wirings_str = [
    "ekmflgdqvzntowyhxuspaibrcjñ",
    "ajdksiruxblhwtmcqgznpyfvoeñ",
    "bdfhjlcprtxvznyeiwgakmusqoñ"
]

def wiring_to_perm(wiring):
    return [ALFABETO.index(c) for c in wiring]

rotor_wirings = [wiring_to_perm(w) for w in rotor_wirings_str]
notches = [17, 5, 22]
reflector_perm = [0] * alphabet_len
for i in range(0, alphabet_len - 1, 2):
    reflector_perm[i] = i + 1
    reflector_perm[i + 1] = i
if alphabet_len % 2 == 1:
    reflector_perm[alphabet_len - 1] = alphabet_len - 1

enigma_positions = [0, 0, 0]
enigma_stecker = {}
cesar_desplaziamento = 3

def cesar(texto, d, decodificar=False):
    res = ""
    for c in texto:
        if c in ALFABETO: res += ALFABETO[(ALFABETO.index(c) + (-d if decodificar else d)) % alphabet_len]
        elif c in ALFABETO_M: res += ALFABETO_M[(ALFABETO_M.index(c) + (-d if decodificar else d)) % alphabet_len]
        else: res += c
    return res


# ====================== BCÑ ==========================

BCÑ = {"a":"R","b":"S","c":"T","d":"U","e":"V","f":"W","g":"X","h":"Y","i":"Z","j":"1","k":"2","l":"3","m":"4","n":"5","ñ":"6","o":"7","p":"8","q":"9","r":"0","s":"-","t":"+","u":"/","v":"*","w":"A","x":"B","y":"C","z":"D","1":"E","2":"F","3":"G","4":"H","5":"I","6":"J","7":"K","8":"L","9":"M","0":"N","-":"Ñ","+":"O","/":"P","*":"Q"," ":" "}
BCÑ_INV = {v: k for k, v in BCÑ.items()}


# ================= BCÑ EXPANDIDO =====================

BCÑ_EXP = {
    "a": "R", "b": "S", "c": "T", "d": "U", "e": "V", "f": "W", "g": "X", "h": "Y", "i": "Z",
    "j": "1", "k": "2", "l": "3", "m": "4", "n": "5", "ñ": "6", "o": "7", "p": "8", "q": "9",
    "r": "0", "s": "-", "t": "+", "u": "/", "v": "*", "w": "?", "x": ":", "y": "(", "z": ")",
    "1": "·", "2": "|", "3": "@", "4": "'", "5": ";", "6": "\"", "7": "=", "8": "%", "9": "_",
    "0": "A", "-": "B", "+": "C", "/": "D", "*": "E", "?": "F", ":": "G", "(": "H", ")": "I",
    "·": "J", "|": "K", "@": "L", "'": "M", ";": "N", '"': "P", "_": "Q"
}
BCÑ_EXP_INV = {v: k for k, v in BCÑ_EXP.items()}


# =================== CUATERNARIO =====================

CUATERNARIO = {"a":"000","b":"001","c":"002","d":"003","e":"010","f":"011","g":"012","h":"013","i":"020","j":"021","k":"022","l":"023","m":"030","n":"031","ñ":"032","o":"033","p":"100","q":"101","r":"102","s":"103","t":"110","u":"111","v":"112","w":"113","x":"120","y":"121","z":"122","1":"123","2":"130","3":"131","4":"132","5":"133","6":"200","7":"201","8":"202","9":"203","0":"210","-":"211","?":"212","/":"213","(":"220",")":"221","+":"222","*":"223",":":"230","¡":"231","%":"232","@":"233","=":"300","[":"301","]":"302",";":"303","'":"304","€":"310","|":"311","<":"312",">":"313","«":"320","»":"321",".":"322",",":"323","_":"330","!":"331","^":"332","~":"333"," ":" "}
CUATERNARIO_INV = {v: k for k, v in CUATERNARIO.items()}


# ================= BINARIO 4 BITS ====================

ALFABETO_BIN = "abcdefghijklmnñopqrstuvwxyz "
binario_4b = {c: format(i % 16, '04b') for i, c in enumerate(ALFABETO_BIN)}
binario_4b_inv = {v: k for k, v in binario_4b.items()}


# ====================== MORSE ========================

MORSE = {"a":".-","b":"-...","c":"-.-.","d":"-..","e":".","f":"..-.","g":"--.","h":"....","i":"..","j":".---","k":"-.-","l":".-..","m":"--","n":"-.","ñ":"--.--","o":"---","p":".--.","q":"--.-","r":".-.","s":"...","t":"-","u":"..-","v":"...-","w":".--","x":"-..-","y":"-.--","z":"--.."," ":"/"}
MORSE_INV = {v: k for k, v in MORSE.items()}


# ==================== SS. TECLA ======================

SST = {"a":":", "b":"1", "c":"2", "d":"3", "e":"4", "f":"5", "g":"6", "h":"7", "i":"8", "j":"9", "k":"0", "l":"@", "m":"/", "n":"'", "ñ":"a", "o":"b", "p":"c", "q":"d", "r":"e", "s":"f", "t":"g", "u":"h", "v":"i", "w":"j", "x":"k", "y":"l", "z":"m", "+":"n", "-":"o", ".":"p", ",":"q", "":"r", "/":"s", ">":"t", "<":"u", "?":"v", "!":"w", " ":" "}
SST_INV = {v: k for k, v in SST.items()}


# =================== S. TECLA =======================

ST = {"a":"*", "b":":", "c":"@", "d":"|", "e":"/", "f":"'", "g":"_", "h":"±", "i":"?", "j":"!", "k":".", "l":",", "m":"¿", "n":"¡", "ñ":"=", "o":"€", "p":"&", "q":"a", "r":"b", "s":"c", "t":"d", "u":"e", "v":"f", "w":"g", "x":"h", "y":"i", "z":"j", "+":"k", "-":"l", ".":"m", ",":"n", "":"o", "/":"p", ">":"q", "<":"r", "?":"s", "!":"t", " ":" "}
ST_INV = {v: k for k, v in ST.items()}


# =================== MS. TECLA =======================

MSST = {"a":"@", "b":"|", "c":"/", "d":"·", "e":"_", "f":"±", "g":"¿", "h":"¡", "i":"!", "j":"?", "k":".", "l":",", "m":"'", "n":"€", "ñ":"&", "o":"(", "p":")", "q":"[", "r":"<", "s":">", "t":"«", "u":"»", "v":"…", "w":"º", "x":"%", "y":"a", "z":"b", "+":"c", "-":"d", ".":"e", ",":"f", "":"g", "/":"h", ">":"i", "<":"j", "?":"k", "!":"l", " ":"m"}
MSST_INV = {v: k for k, v in MSST.items()}


# ================= MAQUINA ENIGMA ====================

def enigma_process(t, pos, st):
    st_perm = [ALFABETO.index(st.get(c, c)) for c in ALFABETO]
    p = pos[:]
    return "".join(encrypt_letter(c, rotor_wirings, reflector_perm, p, st_perm, notches) for c in t)

def encrypt_letter(c, rw, rp, p, sp, n):
    if c.lower() not in ALFABETO: return c
    up = c.isupper()
    idx = ALFABETO.index(c.lower())
    idx = sp[idx]
    p[2] = (p[2] + 1) % alphabet_len
    if p[2] == n[2]:
        p[1] = (p[1] + 1) % alphabet_len
        if p[1] == n[1]: p[0] = (p[0] + 1) % alphabet_len
    for r in range(2, -1, -1):
        o = p[r]
        idx = rw[r][(idx + o) % alphabet_len]
        idx = (idx - o) % alphabet_len
    idx = rp[idx]
    for r in range(3):
        o = p[r]
        idx = (idx + o) % alphabet_len
        inv = [0]*alphabet_len
        for i in range(alphabet_len): inv[rw[r][i]] = i
        idx = (inv[idx] - o) % alphabet_len
    idx = sp[idx]
    res = ALFABETO[idx]
    return res.upper() if up else res


# ================== IMAGEN (STEG) ====================

def hide_text_in_image(path, text):
    with open(path, "rb") as f: d = f.read()
    return d + b"\n--Codificador--\n" + text.encode("utf-8") + b"\n---Fin del Mensaje---"

def extract_text_from_image(path):
    with open(path, "rb") as f: d = f.read()
    s, e = b"\n--Codificador--\n", b"\n---Fin del Mensaje---"
    sp, ep = d.rfind(s), d.rfind(e)
    if sp != -1 and ep != -1: return d[sp+len(s):ep].decode("utf-8", errors="ignore")
    return "No se encontró texto oculto."


# ======================= VENTANA =====================

root = tk.Tk()
root.title("Encriptador")
root.geometry("700x600") # Aumentado para los nuevos frames
root.configure(bg="gray3")

style = ttk.Style()
style.theme_use('clam')
style.configure("Action.TButton", font=("Arial", 10, "bold"), background="#333333", foreground="white", borderwidth=1, padding=5)
style.map("Action.TButton", background=[("active", "#444444")])
style.configure("Mode.TButton", font=("Arial", 10), background="#444444", foreground="#bbbbbb", borderwidth=1, padding=5)
style.map("Mode.TButton", foreground=[("active", "#bbbbbb")], background=[("active", "#555555")])
style.configure("SelectedMode.TButton", font=("Arial", 10, "bold"), background="#0078d7", foreground="white", borderwidth=1, padding=5)
style.map("SelectedMode.TButton", foreground=[("active", "white")], background=[("active", "#0088ff")])

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# SECCION: METODO
method_frame = ttk.LabelFrame(main_frame, text=" Selección de Método ", padding="10")
method_frame.pack(fill="x", pady=5)
ttk.Label(method_frame, text="Método:", font=("Arial", 12, "bold")).pack(side="left", padx=5)
metodo_var = tk.StringVar(value="<ELIGE METODO>")
metodo_combo = ttk.Combobox(method_frame, textvariable=metodo_var, values=["<ELIGE METODO>", "Base64", "Base32", "Base16", "Hex", "UTF-8", "Morse", "BB84", "binario 4 bits", "Cesar + ñ", "BCÑ", "BCÑ Expandido", "SS. Teclado", "S.Teclado", "MS.Teclado", "Cuaternario", "Maquina Enigma", "Imagen (Esteganografía)"], state="readonly", width=30)
metodo_combo.pack(side="left", fill="x", expand=True, padx=5)

# SECCION: MODO
mode_section = ttk.LabelFrame(main_frame, text=" Modo de Operación ", padding="10")
mode_section.pack(fill="x", pady=5)
modo = tk.StringVar(value="Codificar")
btn_codificar = ttk.Button(mode_section, text="Codificar", style="SelectedMode.TButton", command=lambda: set_modo("Codificar"))
btn_codificar.pack(side="left", padx=20, expand=True)
btn_decodificar = ttk.Button(mode_section, text="Decodificar", style="Mode.TButton", command=lambda: set_modo("Decodificar"))
btn_decodificar.pack(side="left", padx=20, expand=True)

# SECCION: ENTRADA
input_section = ttk.LabelFrame(main_frame, text=" Entrada de Datos ", padding="10")
input_section.pack(fill="x", pady=5)

input_toolbar = ttk.Frame(input_section)
input_toolbar.pack(fill="x", pady=0)

btn_add = tk.Button(input_toolbar, text="+", font=("Arial", 14, "bold"), fg="black", bg="white", relief="flat", bd=0, cursor="hand2", command=lambda: load_file())
btn_add.pack(side="right", padx=3)

thumb_label = ttk.Label(input_section)
# thumb_label se empaquetará solo cuando haya imagen

entrada = tk.Text(input_section, height=5, width=80)
entrada.pack(fill="x")

# SECCION: SALIDA
output_section = ttk.LabelFrame(main_frame, text=" Resultado ", padding="10")
output_section.pack(fill="x", pady=5)
salida = tk.Text(output_section, height=5, width=80, state="disabled")
salida.pack(fill="x")

# BOTONES DE ACCION
btns_f = ttk.Frame(main_frame)
btns_f.pack(pady=10)
ttk.Button(btns_f, text="Procesar", style="Action.TButton", command=lambda: run()).pack(side="left", padx=5)
ttk.Button(btns_f, text="Copiar", style="Action.TButton", command=lambda: copy_output()).pack(side="left", padx=5)
ttk.Button(btns_f, text="Limpiar", style="Action.TButton", command=lambda: clear()).pack(side="left", padx=5)
btn_save = ttk.Button(btns_f, text="Guardar Imagen", style="Action.TButton", command=lambda: save_img())
btn_cfg_enigma = ttk.Button(btns_f, text="Configurar Enigma", style="Action.TButton", command=lambda: cfg_enigma())
btn_cfg_cesar = ttk.Button(btns_f, text="Configurar César", style="Action.TButton", command=lambda: cfg_cesar())

input_img_path = None
res_img_bytes = None


# =================== FUNCIONES UI ====================

def set_modo(m):
    modo.set(m)
    btn_codificar.config(style="SelectedMode.TButton" if m=="Codificar" else "Mode.TButton")
    btn_decodificar.config(style="SelectedMode.TButton" if m=="Decodificar" else "Mode.TButton")

def copy_output():
    root.clipboard_clear()
    root.clipboard_append(salida.get("1.0", tk.END).strip())

def clear():
    global input_img_path, res_img_bytes
    entrada.delete("1.0", tk.END)
    salida.config(state="normal"); salida.delete("1.0", tk.END); salida.config(state="disabled")
    input_img_path = res_img_bytes = None
    thumb_label.config(image=''); btn_save.pack_forget()

def load_file():
    global input_img_path
    p = filedialog.askopenfilename(parent=root, filetypes=[("Archivos admitidos", "*.png *.jpg *.jpeg *.txt"), ("Imágenes", "*.png *.jpg *.jpeg"), ("Texto", "*.txt")])
    if p:
        if p.lower().endswith(".txt"):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    content = f.read()
                entrada.delete("1.0", tk.END)
                entrada.insert(tk.END, content)
                input_img_path = None
                thumb_label.config(image='')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo de texto: {e}")
        else:
            input_img_path = p
            img = Image.open(p); img.thumbnail((40, 40))
            tk_img = ImageTk.PhotoImage(img)
            thumb_label.pack(anchor="w") # Mostrar solo cuando hay imagen
            thumb_label.config(image=tk_img); thumb_label.image = tk_img

def save_img():
    if res_img_bytes:
        ext = os.path.splitext(input_img_path)[1]
        p = filedialog.asksaveasfilename(parent=root, defaultextension=ext)
        if p:
            with open(p, "wb") as f: f.write(res_img_bytes)
            messagebox.showinfo("Éxito", "Imagen guardada", parent=root)

def run():
    t = entrada.get("1.0", tk.END).strip()
    m = metodo_var.get()
    res = ""
    salida.config(state="normal"); salida.delete("1.0", tk.END)
    try:
        if m == "<ELIGE METODO>": res = "Error: Elige método"
        elif m == "Cesar + ñ": res = cesar(t, cesar_desplaziamento, modo.get()=="Decodificar")
        elif m == "Maquina Enigma": res = enigma_process(t, enigma_positions, enigma_stecker)
        elif modo.get() == "Codificar":
            if m == "Base64": res = base64.b64encode(t.encode()).decode()
            elif m == "Base32": res = base64.b32encode(t.encode()).decode()
            elif m == "Base16": res = base64.b16encode(t.encode()).decode()
            elif m == "Hex": res = t.encode().hex()
            elif m == "UTF-8": res = t.encode("utf-8").hex()
            elif m == "Morse": res = " ".join(MORSE.get(c.lower(), "") for c in t)
            elif m == "BB84": res = "".join(format(ord(c), '08b') for c in t)
            elif m == "binario 4 bits": res = " ".join(binario_4b.get(c.lower(), "") for c in t)
            elif m == "BCÑ": res = "".join(BCÑ.get(c.lower(), c) for c in t)
            elif m == "BCÑ Expandido": res = "".join(BCÑ_EXP.get(c.lower(), c) for c in t)
            elif m == "SS. Teclado": res = "".join(SST.get(c.lower(), c) for c in t)
            elif m == "S.Teclado": res = "".join(ST.get(c.lower(), c) for c in t)
            elif m == "MS.Teclado": res = "".join(MSST.get(c.lower(), c) for c in t)
            elif m == "Cuaternario": res = " ".join(CUATERNARIO.get(c.lower(), "") for c in t)
            elif m == "Imagen (Esteganografía)":
                if not input_img_path: res = "Error: Sube imagen (pulsa +)"
                else:
                    global res_img_bytes
                    res_img_bytes = hide_text_in_image(input_img_path, t)
                    btn_save.pack(side="left", padx=5); res = "Imagen procesada. Guárdala."
        else:
            if m == "Base64": res = base64.b64decode(t).decode()
            elif m == "Base32": res = base64.b32decode(t).decode()
            elif m == "Base16": res = base64.b16decode(t).decode()
            elif m == "Hex": res = bytes.fromhex(t).decode()
            elif m == "UTF-8": res = bytes.fromhex(t).decode("utf-8")
            elif m == "Morse": res = "".join(MORSE_INV.get(c, "") for c in t.split())
            elif m == "BB84": res = "".join(chr(int(t[i:i+8], 2)) for i in range(0, len(t), 8))
            elif m == "binario 4 bits": res = "".join(binario_4b_inv.get(c, "") for c in t.split())
            elif m == "BCÑ": res = "".join(BCÑ_INV.get(c.upper(), c) for c in t)
            elif m == "BCÑ Expandido": res = "".join(BCÑ_EXP_INV.get(c.upper(), c) for c in t)
            elif m == "SS. Teclado": res = "".join(SST_INV.get(c, c) for c in t)
            elif m == "S.Teclado": res = "".join(ST_INV.get(c, c) for c in t)
            elif m == "MS.Teclado": res = "".join(MSST_INV.get(c, c) for c in t)
            elif m == "Cuaternario": res = " ".join("".join(CUATERNARIO_INV.get(c, "") for c in w.split(" ")) for w in t.split("   "))
            elif m == "Imagen (Esteganografía)":
                if not input_img_path: res = "Error: Sube imagen (pulsa +)"
                else: res = extract_text_from_image(input_img_path)
    except Exception as e: res = f"Error: {e}"
    salida.insert(tk.END, res); salida.config(state="disabled")

def on_method_change(e):
    m = metodo_var.get()
    btn_cfg_enigma.pack_forget()
    btn_cfg_cesar.pack_forget()
    
    if m == "Cesar + ñ":
        btn_cfg_cesar.pack(side="left", padx=5)
    elif m == "Maquina Enigma":
        btn_cfg_enigma.pack(side="left", padx=5)

metodo_combo.bind("<<ComboboxSelected>>", on_method_change)

def cfg_enigma():
    win = tk.Toplevel(root); win.title("Enigma")
    win.group(root)
    cbs = []
    for i in range(3):
        ttk.Label(win, text=f"Rotor (fijo) {i+1}").grid(row=i, column=0, padx=5, pady=5)
        cb = ttk.Combobox(win, values=list(ALFABETO_M), width=3)
        cb.set(ALFABETO_M[enigma_positions[i]]); cb.grid(row=i, column=1); cbs.append(cb)
    
    plugboard_frame = ttk.LabelFrame(win, text="Plugboard")
    plugboard_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    
    plug_entries = {}
    for idx, char in enumerate(ALFABETO_M):
        r = idx // 9
        c = (idx % 9) * 2
        ttk.Label(plugboard_frame, text=f"{char}:").grid(row=r, column=c, padx=2, pady=2, sticky="e")
        ent = ttk.Entry(plugboard_frame, width=2)
        ent.grid(row=r, column=c+1, padx=2, pady=2, sticky="w")
        
        connected_to = enigma_stecker.get(char.lower(), "").upper()
        if connected_to:
            ent.insert(0, connected_to)
            
        plug_entries[char] = ent

    def randomize():
        # Rotores
        for cb in cbs:
            cb.set(random.choice(list(ALFABETO_M)))
        # Plugboard
        for ent in plug_entries.values():
            ent.delete(0, tk.END)
        
        shuffled = list(ALFABETO_M)
        random.shuffle(shuffled)
        for i in range(0, 10, 2): # 5 pares aleatorios
            c1, c2 = shuffled[i], shuffled[i+1]
            plug_entries[c1].insert(0, c2)
            plug_entries[c2].insert(0, c1)

    def ok():
        for i in range(3): enigma_positions[i] = ALFABETO_M.index(cbs[i].get())
        enigma_stecker.clear()
        
        for char, ent in plug_entries.items():
            val = ent.get().strip().upper()
            if val and val in ALFABETO_M and val != char:
                enigma_stecker[char.lower()] = val.lower()
                enigma_stecker[val.lower()] = char.lower()
        win.destroy()

    btn_frame = ttk.Frame(win)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
    ttk.Button(btn_frame, text="Random", command=randomize).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Aceptar", command=ok).pack(side="left", padx=5)

def cfg_cesar():
    win = tk.Toplevel(root); win.title("César config.")
    win.group(root)
    ttk.Label(win, text="Desplazamiento (1-27):").pack(pady=10)
    sp = ttk.Spinbox(win, from_=1, to=27, width=10)
    sp.set(cesar_desplaziamento); sp.pack()
    
    def randomize(): sp.set(random.randint(1, 27))
    def ok():
        global cesar_desplaziamento
        try: cesar_desplaziamento = int(sp.get())
        except: pass
        win.destroy()

    btn_frame = ttk.Frame(win)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Random", command=randomize).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Aceptar", command=ok).pack(side="left", padx=5)

if __name__ == "__main__":
    root.mainloop()
