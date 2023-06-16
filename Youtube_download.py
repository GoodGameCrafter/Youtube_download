# -*- coding: utf-8 -*-
import time
import codecs
from pytube import (YouTube,request)
import os
import moviepy.video.io.ffmpeg_tools as mvp
import tkinter as tk
from tkinter import (filedialog as fd,ttk,messagebox)
import threading
import Download

request.default_range_size =1048576        #Intervall for pytube(on_progress_callback): Updates every 1Mb

class Start(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)  # -> for Toplevel Window
        self.font:(str,int,str) = ("Arial",20,"bold")         #Font für überschrift
        self.font2:(str,int) = ("Arial", 10)            # Font für normalen Text
        self.index = 0


    def clearFrame(self):  # Löscht alle Inhalte des Fensters
        for widget in fenster.winfo_children():
            widget.destroy()

    def Menü(self):  #### Menü ####
        menuleiste = tk.Menu(fenster)
        menuleiste.add_command(label="Exit",command=lambda : fenster.quit())
        menuleiste.add_command(label="Hilfe", command=lambda: self.help())
        menuleiste.add_command(label="Info", command=lambda: self.info())
        fenster.config(menu=menuleiste)

    def Menü2(self,data):  #### Menü2 ####
        menuleiste = tk.Menu(fenster)
        menuleiste.add_command(label="Exit",command=lambda : fenster.quit())
        menuleiste.add_command(label="Drucken", command=lambda: self.Drucken(data))
        menuleiste.add_command(label="Hilfe", command=lambda: self.help2())
        menuleiste.add_command(label="Info", command=lambda: self.info())
        fenster.config(menu=menuleiste)

    def help(self):         # Hilfetext
        m_text = "\nDateiformat:\
                 \n     mp4: Lädt das gesamte Video herunter\
                 \n     mp3: Lädt nur die Audiospur des Videos herunter\n\
                 \nAuflösung:\
                 \n     Ändern um Auflösung des Videos festzulegen,\
                 \n     ist die gewählte Auflösung nicht verfügbar,\
                 \n     wird das Video in der höchsten verfügbaren\
                 \n     Auflösung heruntergeladen\n\
                 \nZielordner:\
                 \n     Verzeichnis in das die heruntergeladenen Daten\
                 \n     gespeichert werden\n\
                 \nModus: \
                 \n     Einzelnes Video herunterladen:\
                 \n         Lädt ein einzelnes Video herunter\
                 \n         Videolink eingeben um zu beginnen\n\
                 \n     Playlist herunterladen:\
                 \n         Lädt alle Videos einer Playlist herunter,\
                 \n         Link zur Playlist eingeben um zu beginnen\n\
                 \n     Videolinks aus Dokument importieren:\
                 \n         Möglichkeit um eine Liste unabhängiger\
                 \n         Videos herunterzuladen\
                 \n         Dateipfad eingeben um zu beginnen\
                 \n         Es kann nur ein Link pro Zeile verarbeitet werden!!\
                 \n     Neueste Videos:\
                 \n         Kanalnamen oder Datei mit mehreren Kanalnamen ein-\
                 \n         geben um die 5 neusten Videos herunterzuladen"
        messagebox.showinfo("Hilfe", m_text)

    def help2(self):        #Hilfetext2
        m_text = "\nTitel:\
                 \n     Zeigt Titel des Videos an das heruntergeladen\
                 \n     werden soll,bei Fehler ist entweder der Link\
                 \n     ungültig oder das Video nicht öffentlich.\n\
                 \nStatus:\
                 \n     Wartet:\
                 \n         Download ist in der Warteschlange.\n\
                 \n     Lädt herunter:\
                 \n         Video/Audio wird heruntergeladen.\n\
                 \n     Abgeschlossen:\
                 \n         Download erfolgreich.\n\
                 \n     Fehler:\
                 \n         Download fehlgeschlagen\
                 \n         (->Video nicht öffentlich,Altersbeschränkungen)\
                        Eine Liste mit fehlgeschlagenen Downloads\
                 \n         befindet sich im gewählten Verzeichnis\n\
                 \nDrucken:\
                 \n     Speichert die Tabelle ins gewählte Verzeichnis"
        messagebox.showinfo("Hilfe",m_text)

    def info(self):             #Infotext
        m_text = "\
        ************************\n\
        Date: 02.06.2023\n\
        Version: 3.2a\n\
        ************************"
        messagebox.showinfo("About", m_text)

    def callback(self,event):
        self.label6.place(x=10, y=220)
        mode = event.widget.get()
        if mode=="Audio(mp3)":
            self.box2.config(state="disabled")
            self.only_audio = True
            return
        elif mode == "Video(mp4)":
            self.box2.config(state="normal")
            self.box2['state'] = 'readonly'
            self.only_audio = False
            return
        if mode in ["einzelnes Video herunterladen","Playlist herunterladen"]:
            self.label6.config(text="Bitte Link eingeben:")
            self.button2.config(state="disabled")
        elif mode== "Videolinks aus Dokument importieren":
            self.label6.config(text="Bitte Dateipfad eingeben:")
            self.button2.config(state="normal")
        elif mode == "Neueste Videos":
            self.label6.config(text="Bitte Kanalname oder\nDateipfad eingeben:")
            self.button2.config(state="normal")
            self.button.config(command=lambda: [self.check_entry(self.box.get(),
                self.box2.get(),self.eingabefeld.get(),self.box3.get(),self.eingabefeld2.get(),self.box4.get())])
            self.label6.place(x = 10,y = 215)
            self.eingabefeld2.place(x=240, y=220, width=125, height=25)
            self.button2.place(x=365, y=220)
            self.label7.place(x = 383,y = 222,width=50,height=20)
            self.box4.place(x = 430,y = 220,width=40,height=25)
            return
        self.button.config(command=lambda: [self.check_entry(self.box.get(),
                    self.box2.get(), self.eingabefeld.get(), self.box3.get(), self.eingabefeld2.get())])
        self.label7.place(x=455, y=230, width=1, height=1)
        self.box4.place(x=455, y=230, width=1, height=1)
        self.eingabefeld2.place(x = 240,y = 220,width=210,height=25)
        self.button2.place(x = 450,y = 220)
        fenster.update()

    def callback2(self,event):
        if self.text2!= "":
            self.text2.set(value="")

    def select_file(self,val=0):  # Funktion um Dokument direkt auswählen zu können
        if val ==2:
            file = fd.askdirectory()
            self.text.set(value = file)
        else:
            file = fd.askopenfile(mode='r+', filetypes=[('Textdokumente(*.txt)', ("*.txt"))])
            if file is not None:
                filename = file.name
                self.text2.set(value=filename)

    def check_entry(self,format:str,resolution:str,destination:str,mode:str,input:str,hits = "1"):  # Überprüft Eingabe des Dokuments
        global outpath
        outpath = destination
        self.resolution = resolution
        self.only_audio = False
        pb = ttk.Progressbar(fenster, orient="horizontal", mode="indeterminate")
        if format == "Audio(mp3)":
            self.only_audio = True
        label1 = tk.Label(fenster, text="")
        label2 = tk.Label(fenster, text="")
        label1.place(x=255, y=150, width=200, height=15)
        label2.place(x=235, y=250, width=225, height=30)
        fenster.update()
        if destination =="":
            label1.config(text="[Fehler]: Bitte Dateipfad eingeben", fg="red")
            return None
        else:
            if not os.path.exists(destination):
                label1.config(text="[Fehler]:Dateipfad ist ungültig", fg="red")
                return None
        if mode == "Videolinks aus Dokument importieren":
            if input == "":
                label2.config(text="[Fehler]: Bitte Dateipfad eingeben", fg="red")
                return None
            elif input[-4:]!= ".txt":
                label2.config(text="[Fehler]: Dateiformat wird nicht unterstützt!", fg="red")
                return None
            elif not os.path.exists(input):
                label2.config(text="[Fehler]:Dateipfad ist ungültig", fg="red")
                return None
        elif mode == "Neueste Videos":
            if input == "":
                label2.config(text="[Fehler]: Bitte Kanalname oder\nDateipfad eingeben", fg="red")
                return None
            elif os.path.exists(input) and input[-4:]!= ".txt":
                label2.config(text="[Fehler]: Dateiformat wird nicht unterstützt!", fg="red")
                return None
            elif not os.path.exists(input) and input[-4:]== ".txt":
                label2.config(text="[Fehler]:Dateipfad ist ungültig", fg="red")
                return None
        else:
            if input == "":
                label2.config(text="[Fehler]: Bitte Link eingeben", fg="red")
                return None
        self.button.destroy()
        label = tk.Label(fenster, text="Überprüfe Links...").place(x=50, y=280)
        pb.place(x=180, y=280, width=280, height=20);pb.start(10)
        fenster.update()
        t0 = threading.Thread(target=self.Run, args=(mode,input,hits))
        t0.daemon = True
        t0.start()

    def Run(self,mode:str,input:str,hits:str):
        functions = {"Videolinks aus Dokument importieren":Download.getLinks().openfile,
                     "Neueste Videos":Download.getLinks().new_vid,
                     "einzelnes Video herunterladen":Download.getLinks().search_Pytube,
                     "Playlist herunterladen":Download.getLinks().playlist}
        func = functions.get(mode)
        if mode == "Neueste Videos":
            links,fehler,data = func(input,int(hits))
        else:
            links, fehler, data = func(input)
        return self.getData(links, fehler, data, int(hits))

    def getData(self,*args):
        self.Links,self.Fehler,self.Data,self.hits = args
        return self.Download_Übersicht()

    def Drucken(self,data):
        with codecs.open("%s/Videolist.txt"% outpath, "w","utf-8") as f:
            line = ""
            for elem in data:
                line += elem+" "+data[elem][0]+"\n"
            f.write(line)
        m_text = "Liste gespeicher unter:\n'%s/Videolist.txt'" % outpath
        messagebox.showinfo("Drucken",m_text)

    def Seite_1(self):
        Start().clearFrame()
        fenster.update()
        Start().Menü()
        label = tk.Label(fenster,text="Video-Download",font= self.font)
        label2 = tk.Label(fenster, text="Bitte Auflösung auswählen:", font=self.font2)
        label3 = tk.Label(fenster, text="Bitte Dateiformat auswählen:", font=self.font2)
        label4 = tk.Label(fenster,text="Bitte Zielordner auswählen:",font= self.font2)
        label5 = tk.Label(fenster,text="Bitte Modus auswählen:",font= self.font2)
        self.label6 = tk.Label(fenster, text="Bitte Link eingeben:",font= self.font2)
        self.label7 = tk.Label(fenster, text="Treffer:",font= self.font2)
        self.text = tk.StringVar(None)
        self.text.set(value="")
        self.text2 = tk.StringVar(None)
        self.text2.set(value="")
        self.eingabefeld = tk.Entry(fenster, textvariable=self.text)
        self.eingabefeld2 = tk.Entry(fenster, textvariable=self.text2,width=200)
        self.eingabefeld2.bind("<Button-1>",self.callback2)
        self.auswahl = tk.StringVar(None)
        self.auswahl2 = tk.StringVar(None)
        self.auswahl3 = tk.StringVar(None)
        self.auswahl4 = tk.StringVar(None)
        self.auswahl.set(value="Video(mp4)")
        self.auswahl2.set(value="1080p")
        self.auswahl3.set(value="einzelnes Video herunterladen")
        self.auswahl4.set(value="3")
        self.box = ttk.Combobox(fenster, textvariable=self.auswahl)
        self.box2 = ttk.Combobox(fenster, textvariable=self.auswahl2)
        self.box3 = ttk.Combobox(fenster, textvariable=self.auswahl3)
        self.box4 = ttk.Combobox(fenster, textvariable=self.auswahl4)
        values = ["Video(mp4)","Audio(mp3)"]
        values2 = ["bestmögliche Auflösung", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p",
                  "niedrigste Auflösung"]
        values3 = ["einzelnes Video herunterladen","Playlist herunterladen","Videolinks aus Dokument importieren","Neueste Videos"]
        values4 = [i for i in range(1,11)]
        self.box['values'] = values
        self.box2['values'] = values2
        self.box3['values'] = values3
        self.box4['values'] = values4
        self.box['state'] = 'readonly'
        self.box2['state'] = 'readonly'
        self.box3['state'] = 'readonly'
        self.box4['state'] = 'readonly'
        self.button = tk.Button(fenster, text="Weiter -->", command=lambda: [self.check_entry(self.box.get(),
                                            self.box2.get(),self.eingabefeld.get(),self.box3.get(),self.eingabefeld2.get())])
        button1 = tk.Button(fenster, text='▽', command=lambda: self.select_file(2))
        self.button2 = tk.Button(fenster, text='▽',state="disabled", command=lambda: self.select_file())
        self.box.bind("<<ComboboxSelected>>", self.callback)
        self.box3.bind("<<ComboboxSelected>>", self.callback)
        label.place(x = 135,y = 5)
        label2.place(x=10, y=85)
        label3.place(x=10, y=50)
        label4.place(x = 10,y = 120)
        label5.place(x = 10,y = 175)
        self.label6.place(x = 10,y = 220)
        self.eingabefeld.place(x = 240,y = 120,width=210,height=25)
        self.eingabefeld2.place(x = 240,y = 220,width=210,height=25)
        self.button.place(x = 215,y = 285)
        button1.place(x = 450,y = 120)
        self.button2.place(x = 450,y = 220)
        self.box.place(x=240, y=50, width=230, height=25)
        self.box2.place(x = 240,y = 85,width=230,height=25)
        self.box3.place(x=240, y=175, width=230, height=25)

    def Download_Übersicht(self):
        Start().clearFrame()
        fenster.update()
        Start().Menü2(self.Data)
        label = tk.Label(fenster, text="Status:", font=("Arial", 15, "bold"))
        label2 = tk.Label(fenster, text="Fortschritt:")
        label3 = tk.Label(fenster, text="Gesamtfortschritt:")
        self.pb_label = ttk.Style(fenster)
        self.pb_label2 = ttk.Style(fenster)
        self.pb_label.layout("text.Horizontal.TProgressbar",[('Horizontal.Progressbar.trough',{'children': [('Horizontal.Progressbar.pbar',
                          {'side': 'left', 'sticky': 'ns'}),("Horizontal.Progressbar.label",{"sticky": ""})],'sticky': 'nswe'})])
        self.pb_label2.layout("text2.Horizontal.TProgressbar",[('Horizontal.Progressbar.trough', {'children': [('Horizontal.Progressbar.pbar',
                            {'side': 'left', 'sticky': 'ns'}),("Horizontal.Progressbar.label",{"sticky": ""})], 'sticky': 'nswe'})])
        self.pb_label.configure('text.Horizontal.TProgressbar', text='0 %')
        self.pb_label2.configure('text2.Horizontal.TProgressbar', text='0 %')
        cols = ("Nr.","Links", "Titel", "Status")
        cols_width = (25,200,200,200)
        self.status_table = ttk.Treeview(fenster,columns=cols,show='headings')
        for i,link in enumerate(self.Links):
            title,status = self.Data[link]
            self.table_insert(i, link, title, status)
        for i,(col,col_width) in enumerate(zip(cols,cols_width)):
            self.status_table.column(col, stretch=False,width = col_width)
            self.status_table.heading(col,text=col,anchor=tk.W)
        scroll_bar = ttk.Scrollbar(fenster, command=self.status_table.yview)
        scroll_bar2 = ttk.Scrollbar(fenster, command=self.status_table.xview, orient= "horizontal")
        self.status_table['yscrollcommand'] = scroll_bar.set
        self.status_table['xscrollcommand'] = scroll_bar2.set
        self.pb = ttk.Progressbar(fenster,style="text.Horizontal.TProgressbar",length=300,value=0)
        self.pb2 = ttk.Progressbar(fenster, style="text2.Horizontal.TProgressbar", length=300, value=0)
        self.button = tk.Button(fenster, text="Weiter",state= "disabled",command=lambda :self.Weiter())
        self.button2 = tk.Button(fenster, text="Start",command=lambda :self.Start())
        self.button3 = tk.Button(fenster, text="Pause",state= "disabled",command=lambda :self.Pause())
        self.button4 = tk.Button(fenster, text="<--Zurück",command=lambda :self.Seite_1())
        self.button5 = tk.Button(fenster,text="Aktualisieren",command=lambda :self.Aktualisieren(self.Links,self.Fehler,self.Data))
        self.counter = tk.Label(fenster)
        self.counter.place(x=390, y=290, height=25)
        label.place(x=15, y=0)
        label2.place(x=50, y=225)
        label3.place(x=30, y=255)
        scroll_bar.place(x=460, y=30, height=180,width=30)
        scroll_bar2.place(x=15, y=195, height=30,width=450)
        self.status_table.place(x=15, y=30, width=450, height=180)
        self.pb.place(x=140, y=225,height = 20)
        self.pb2.place(x=140, y=255, height=20)
        self.button.place(x=300, y=290, width=80, height=25)
        self.button2.place(x=220, y=290, width=80, height=25)
        self.button3.place(x=140, y=290, width=80, height=25)
        self.button4.place(x=10, y=290, width=80, height=25)
        self.button5.place(x=400, y=2)

    def table_insert(self,index:int, link:str, title:str, status:str):
        tag1 = self.status_table.tag_configure("Abgeschlossen", background="#90EE90")  # -> hellgrün
        tag2 = self.status_table.tag_configure("Fehler", background="#FFCCCB")  # -> hellrot
        tag3 = self.status_table.tag_configure("Übersprungen", background="#add8e6")  # -> hellblau

        line = ("%d)" % (index+1), link, title, status)
        if status == "Wartet":
            self.status_table.insert("", index, values=line)
        elif status == "Abgeschlossen":
            self.status_table.insert("", index, values=line, tags="Abgeschlossen")
        elif status in ["Datei existiert bereits", "Übersprungen"]:
            self.status_table.insert("", index, values=line, tags="Übersprungen")
        else:
            self.status_table.insert("", index, values=line, tags="Fehler")

    def Aktualisieren(self,Links:list,Fehler:list,Data:dict):
        fenster2 = tk.Toplevel(fenster)
        fenster2.transient(fenster)  # set to be on top of the main window
        fenster2.grab_set()  # clicks on the main window are ignored
        fenster2.title("Aktualisieren")
        ###center window2
        width2 = 200;
        height2 = 60
        win_width = width / 2;
        win_height = height / 2
        x2 = x + win_width - (width2 / 2)
        y2 = y + win_height - (height2 / 2)
        fenster2.geometry('%dx%d+%d+%d' % (width2, height2, x2, y2))
        fenster2.resizable(False, False)
        ########
        self.pause = True
        label = tk.Label(fenster2,text="Fortschritt:")
        pb = ttk.Progressbar(fenster2, orient='horizontal', mode='determinate')
        label.place(x=5,y=5)
        pb.place(x=5, y=25,width=180, height=20)
        fenster2.update()
        resolved = []
        if Fehler != []:
            self.index = Links.index(Fehler[0])
        for i, elem in enumerate(Fehler, start=1):            #Fehlerhafte Links werden erneut geprüft
            if elem[:8] != "https://":
                link,fehler,res = Download.getLinks().new_vid(elem,self.hits)
                if fehler == []:
                    Links.remove(elem);Data.pop(elem)
                    j = 0
                    while f"##{j}##" in Links:
                        j+=1
                    link[0] = f"##{j}##"
                    res[f"##{j}##"]= res["##0##"]
                    Links |= link
                    Data |= res

            elif "list="in elem:
                Links, fehler, Data = Download.getLinks().playlist(elem)
            else:
                link,fehler,res = Download.getLinks().search_Pytube(elem)
                Data[elem]= res[elem]
            pb["value"] = 100 * (i / len(Fehler))
            if fehler == []:
                resolved.append(elem)
            fenster2.update()
        for elem in resolved:
            Fehler.remove(elem)
        pb.destroy()
        fenster2.destroy()
        self.Links = Links;self.Fehler = Fehler;self.Data=Data
        return self.Download_Übersicht()

    def Start(self):                                                    # initialer Start der Loop
        self.button2.config(text="Überspringen",command=lambda :self.Überspringen())
        self.pause = False
        self.skipped = False
        t1 = threading.Thread(target=self.Loop_Start)
        t1.daemon = True
        t1.start()

    def Pause(self):                                                    # pausiert Counter und Downloads
        self.pause = True
        self.button.config(state="normal")
        self.button2.config(state="disabled")
        self.button3.config(state="disabled")

    def Weiter(self):                                                   # Weiter
        self.button.config(state="disabled")
        self.button2.config(state="normal")
        self.button3.config(state="normal")
        self.pause = False
        self.Loop_Start()

    def Überspringen(self):                                             # Überspringt ausgewähltes Element
        self.skipped = True

    def Loop_Start(self):
        self.skipped = False
        self.timeout = False
        if self.index == len(self.Links):                                # Wenn das Ende der Warteschlange erreicht ist
            path = outpath + "/Fehlgeschlagene Downloads.txt"
            if os.path.exists(path):                                     #Altes Dokument mit fehlgeschlagenen Downloads
                os.remove(path)                                          #wird gelöscht
            if self.Fehler != []:
                fehler = ""
                with codecs.open(path, "w+","utf-8") as f:               # Neues Dokument mit fehlgeschlagenen Downloads
                    for elem in self.Fehler:                             # wird erstellt
                        fehler+= F"{elem} {self.Data[elem]}\n"
                    f.write(fehler)
            self.button.destroy()
            self.button2.config(text="Beenden", command=lambda: fenster.quit())
            self.button2.config(state="normal")
            self.button3.destroy()
            self.button5.destroy()
            self.counter.destroy()
            return None

        self.button2.config(state="normal")
        self.button3.config(state="normal")
        self.button5.config(state="normal")
        title,status = self.Data[self.Links[self.index]]
        for j in range(6):                                                # Während der Counter läuft kann pausiert oder
            time.sleep(1.0)                                               # übersprungen werden
            self.counter.config(text="Überspringen? " + str(5 - j) + "s") # Video bei Fehler überspringen
            if title == "Fehler":
                self.Data[self.Links[self.index]][1] = "Fehler"
                return self.Loop_End()
            elif status in ["#####", "Unbekannter Kanalname"]:            # Zeilen Überschrift beibehalten
                return self.Loop_End()
            if self.skipped:                                              # Kontrolle ob manuell übersprungen
                self.Data[self.Links[self.index]][1] = "Übersprungen"
                return self.Loop_End()
            if self.pause:                                                # Kontrolle ob pausiert
                self.button.config(state="normal")
                break
            fenster.update()
        self.counter.config(text="")
        self.button2.config(state="disabled")
        self.button3.config(state="disabled")
        if not self.pause:
            self.button5.config(state="disabled")
            self.pb["value"] = 0
            if self.only_audio:
                self.pb_label.configure('text.Horizontal.TProgressbar', text="Audio wird heruntergeladen: 0 %")
            else:
                self.pb_label.configure('text.Horizontal.TProgressbar', text="Video wird heruntergeladen: 0 %")
            fenster.update()
            line = ("%d)" % (self.index + 1), self.Links[self.index], title, "Lädt herunter") # auswählen der Zeile zum hinterlegen mit Farbe
            selected_item = self.status_table.get_children()[self.index]
            self.status_table.delete(selected_item)
            tag0 = self.status_table.tag_configure("Download", background="#90EE90")
            self.status_table.insert("", self.index, values=line, tags="Download")
            self.t2 = threading.Thread(target=self.Download_Manager, args=[self.Links[self.index]])
            self.t2.daemon = True
            self.t2.start()

    def Timeout(self):
        self.timeout = True
        self.Data[self.Links[self.index]][1] = "Verbindung verloren"                  # neuen Status setzen
        m_text = "Zeitüberschreitung bei der\nNetzwerkverbindung"
        messagebox.showwarning("Youtube_download", m_text)
        self.Pause()
        return self.Loop_End()

    def Download_Progress(self, chunk, file_handle, bytes_remaining):       # Rechner für Statusanzeige
        percent = (100 * (self.file_size - bytes_remaining)) // self.file_size
        self.pb["value"] = percent
        percent = max(percent, 0)
        percent = min(100, percent)
        if self.only_audio or self.video_downloaded:
            self.pb_label.configure('text.Horizontal.TProgressbar',
                                    text="Audio wird heruntergeladen: " + str(percent) + " %")
        else:
            self.pb_label.configure('text.Horizontal.TProgressbar',
                                    text="Video wird heruntergeladen: " + str(percent) + " %")
        fenster.update()

    def Download_Manager(self,link):
        for j in range(3):
            try:
                self.youtubeObject = YouTube(link, on_progress_callback=self.Download_Progress)
                title = self.youtubeObject.title
                break
            except:
                continue
        else:
            self.Data[self.Links[self.index]][1] = "Verbindung verloren"
            m_text = "Zeitüberschreitung bei der\nNetzwerkverbindung"
            messagebox.showwarning("Youtube_download", m_text)
            return self.Timeout()
        if self.youtubeObject.age_restricted:
            self.Data[self.Links[self.index]][1] = "Video ist altersbeschränkt"
            return self.Loop_End()
        for i in ["/", ":", "*", "<", ">", "|", "?", '"', "\\"]:
            title = title.replace(i, "")
        self.title = title.strip()
        self.video_exists = False
        if self.only_audio:
            return self.Audio_Download()
        for func in [self.Video_Download, self.Audio_Download, self.Merge]:
            if self.video_exists or self.timeout:
                break
            func()
        else:
            return self.Loop_End()

    def Video_Download(self):                   #Lädt die Video-Datei herunter
        self.video_downloaded = False
        if os.path.exists(outpath + "/" + self.title + ".mp4"):
            self.Data[self.Links[self.index]][1] = "Datei existiert bereits"
            self.video_exists = True
            return self.Loop_End()
        try:
            if self.resolution == "bestmögliche Auflösung":
                video = self.youtubeObject.streams.get_highest_resolution()
            elif self.resolution == "niedrigste Auflösung":
                video = self.youtubeObject.streams.get_lowest_resolution()
            else:
                video = self.youtubeObject.streams.filter(res=self.resolution, file_extension="mp4").first()
                if video == None:
                    video = self.youtubeObject.streams.get_highest_resolution()
            try:
                self.file_size = video.filesize
                video.download("%s" % outpath, "tmp_video.mp4", timeout=10)
                self.video_downloaded = True
            except:
                os.remove("%s/tmp_video.mp4" % outpath)
                return self.Timeout()
        except Exception as e:
            self.Data[self.Links[self.index]][1] = "Fehler"
            if "age restricted" in str(e):
                self.Data[self.Links[self.index]][1] = "Video ist altersbeschränkt"
            self.video_exists = True
            return self.Loop_End()

    def Audio_Download(self):               #Lädt die Audio-Datei herunter
        if self.only_audio:
            if os.path.exists(outpath + "/" + self.title + ".mp3"):
                self.Data[self.Links[self.index]][1] = "Datei existiert bereits"
                return self.Loop_End()
            if os.path.exists(outpath + "/" + self.title + ".mp4"):
                os.rename("%s/%s.mp4" % (outpath, self.title), "%s/tmp_video.mp4" % outpath)
                self.video_exists = True
        try:
            audio = self.youtubeObject.streams.filter(only_audio=True).first()
            self.file_size = audio.filesize
            audio.download("%s" % outpath, "tmp_audio.mp3", timeout=10)
            if self.only_audio:
                os.rename("%s/tmp_audio.mp3" % outpath, "%s/%s.mp3" % (outpath, self.title))
                if self.video_exists:
                    os.rename("%s/tmp_video.mp4" % outpath , "%s/%s.mp4" % (outpath, self.title))
                self.Data[self.Links[self.index]][1] = "Abgeschlossen"
                return self.Loop_End()
        except:
            if self.video_exists:
                os.rename("%s/tmp_video.mp4" % outpath, "%s/%s.mp4" % (outpath, self.title))
            for elem in ["tmp_video.mp4", "tmp_audio.mp3"]:
                if os.path.exists("%s/%s" % (outpath, elem)):
                    os.remove("%s/%s" % (outpath, elem))
            return self.Timeout()

    def Merge(self):                                #Kombiniert die Video und die Audiodatei
        self.pb_label.configure('text.Horizontal.TProgressbar',text="Verarbeiten...")
        mvp.ffmpeg_merge_video_audio("%s/tmp_video.mp4" % outpath, "%s/tmp_audio.mp3" % outpath,
                                     "%s/%s.mp4" % (outpath, self.title))
        os.remove("%s/tmp_video.mp4" % outpath)
        os.remove("%s/tmp_audio.mp3" % outpath)
        self.Data[self.Links[self.index]][1] = "Abgeschlossen"

    def Loop_End(self):
        title,status= self.Data[self.Links[self.index]]
        if status in ["Fehler","Verbindung verloren","Video ist altersbeschränkt"]:
            self.Fehler.append(self.Links[self.index])
        selected_item = self.status_table.get_children()[self.index]
        self.status_table.delete(selected_item)
        self.table_insert(self.index,self.Links[self.index], title, status)

        self.pb["value"] = 100
        self.pb_label.configure('text.Horizontal.TProgressbar', text="Abgeschlossen")
        self.pb2["value"] = int(((self.index + 1) / len(self.Links)) * 100)
        self.pb_label2.configure('text2.Horizontal.TProgressbar',
                                 text=str(int(((self.index + 1) / len(self.Links)) * 100)) + " %")
        if not self.timeout:
            self.index += 1
        fenster.update()
        return self.Loop_Start()

if __name__ == "__main__":
    fenster = tk.Tk()
    fenster.title("Youtube_Download")
    ###center main window
    screen_width = fenster.winfo_screenwidth()
    screen_height = fenster.winfo_screenheight()
    width = 500;
    height = 350
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    fenster.geometry('%dx%d+%d+%d' % (width, height, x, y))
    #####
    fenster.resizable(False,False)
    main = Start(fenster).Seite_1()  # -> for Toplevel Window
    fenster.mainloop()
