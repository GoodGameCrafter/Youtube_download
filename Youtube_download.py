import time
from pytube import (YouTube,Playlist,request)
import os
import moviepy.video.io.ffmpeg_tools as mvp
import tkinter as tk
from tkinter import (filedialog as fd,ttk,messagebox)
import threading

request.default_range_size =1048576        #Intervall for pytube(on_progress_callback): Updates every 1Mb

class Start():
    def clearFrame(self):  # Löscht alle Inhalte des Fensters
        for widget in fenster.winfo_children():
            widget.destroy()

    def Menü(self):  #### Menü ####
        menuleiste = tk.Menu(fenster)
        menuleiste.add_command(label="Exit",command=lambda : fenster.quit())
        menuleiste.add_command(label="Hilfe", command=lambda: self.help())
        menuleiste.add_command(label="Info", command=lambda: self.info())
        fenster.config(menu=menuleiste)

    def Menü2(self):  #### Menü2 ####
        menuleiste = tk.Menu(fenster)
        menuleiste.add_command(label="Exit",command=lambda : fenster.quit())
        menuleiste.add_command(label="Hilfe", command=lambda: self.help2())
        menuleiste.add_command(label="Info", command=lambda: self.info())
        fenster.config(menu=menuleiste)

    def help(self):
        m_text = "\nDateiformat:\
                 \n     mp4: Lädt das gesamte Video herunter\
                 \n     mp3: Lädt nur die Audiospur des Videos herunter\n\
                 \nAuflösung:\
                 \n     Ändern um Auflösung des Videos festzulegen,\
                 \n     ist die gewählte Auflösung nicht verfügbar,\
                 \n     wird das Video in der höchsten verfügbaren\
                 \n     Auflösung heruntergeladen\n\
                 \nZielordener:\
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
                 \n         Videos herunterzuaden\
                 \n         Dateipfad eingeben um zu beginnen\
                 \n         Es kann nur ein Link pro Zeile verarbeitet werden!!"
        messagebox.showinfo("Hilfe", m_text)

    def help2(self):
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
                 \n         befindet sich im gewählten Verzeichnis"
        messagebox.showinfo("Hilfe",m_text)

    def info(self):
        m_text = "\
        ************************\n\
        Date: 30.01.2023\n\
        Version: 2.1a\n\
        ************************"
        messagebox.showinfo("About", m_text)

    def callback(self,event):
        if event.widget.get()=="Audio(mp3)":
            self.box2.config(state="disabled")
            self.only_audio = True
        elif event.widget.get()== "einzelnes Video herunterladen" or event.widget.get()=="Playlist herunterladen":
            self.label6.config(text="Bitte Link eingeben:")
            self.button2.config(state="disabled")
        elif event.widget.get()== "Videolinks aus Dokument importieren":
            self.label6.config(text="Bitte Dateipfad eingeben:")
            self.button2.config(state="normal")
        else:
            self.box2.config(state="normal")
            self.box2['state'] = 'readonly'


    def select_file(self,val=0):  # Funktion um Dokument direkt auswählen zu können
        if val ==2:
            file = fd.askdirectory()
            self.text.set(value = file)
        else:
            file = fd.askopenfile(mode='r+', filetypes=[('Textdokumente(*.txt)', ("*.txt"))])
            if file is not None:
                filename = file.name
                self.text2.set(value=filename)

    def check_entry(self,format,resolution,destination,mode,data):  # Überprüft Eingabe des Dokuments
        self.destination = destination
        self.resolution = resolution
        self.only_audio = False
        if format == "Audio(mp3)":
            self.only_audio = True
        label1 = tk.Label(fenster, text="")
        label2 = tk.Label(fenster, text="")
        label1.place(x=255, y=150, width=200, height=15)
        label2.place(x=255, y=250, width=200, height=15)
        if destination =="":
            label1.config(text="[Fehler]: Bitte Dateipfad eingeben", fg="red")
            return None
        else:
            if not os.path.exists(destination):
                label1.config(text="[Fehler]:Dateipfad ist ungültig", fg="red")
                return None
        if mode == "Videolinks aus Dokument importieren":
            if data == "":
                label2.config(text="[Fehler]: Bitte Dateipfad eingeben", fg="red")
                return None
            elif data[-4:]!= ".txt":
                label2.config(text="[Fehler]: Dateiformat wird nicht unterstützt!", fg="red")
                return None
            elif not os.path.exists(data):
                label2.config(text="[Fehler]:Dateipfad ist ungültig", fg="red")
                return None
            else:
                self.button.destroy()
                self.open_file(data,"import")
        else:
            if data == "":
                label2.config(text="[Fehler]: Bitte Link eingeben", fg="red")
                return None
            elif mode == "einzelnes Video herunterladen":
                self.open_file(data,"one_link")
            elif mode == "Playlist herunterladen":
                self.button.destroy()
                self.open_file(data,"playlist")

    def open_file(self,link,mode):
        self.Links = []
        self.titles = []
        self.Status =[]
        self.Fehler = ""
        if mode == "one_link":
            self.Links.append(link)
            try:
                youtubeObject = YouTube(link)
                title = youtubeObject.title.strip()
                self.titles.append(title)
                self.Status.append("Wartet")
            except:
                self.Fehler += link + "\n"
                self.titles.append("Fehler")
                self.Status.append("Video nicht verfügbar/nicht öffentlich")
        elif mode == "playlist":
            try:
                playlist = Playlist(link)
                if len(playlist) == 0:
                    self.Links.append(link)
                    self.Fehler += link + "\n"
                    self.titles.append("Fehler")
                    self.Status.append("Playlist nicht verfügbar/nicht öffentlich")
                else:
                    label = tk.Label(fenster, text="Überprüfe Links...").place(x=50, y=280)
                    pb = ttk.Progressbar(fenster, orient='horizontal', mode='determinate', length=280)
                    pb.place(x=180, y=280)
                    fenster.update()
                    for i, url in enumerate(playlist.video_urls):
                        self.Links.append(url)
                        youtubeObject = YouTube(url)
                        title = youtubeObject.title.strip()
                        self.titles.append(title)
                        self.Status.append("Wartet")
                        pb["value"] = 100 * (i / len(playlist))
                        fenster.update()
            except:
                self.Links.append(link)
                self.Fehler += link + "\n"
                self.titles.append("Fehler")
                self.Status.append("Ungültiger Link")

        else:
            label = tk.Label(fenster, text="Überprüfe Links...").place(x=50, y=280)
            pb = ttk.Progressbar(fenster, orient='horizontal', mode='determinate', length=280)
            pb.place(x=180, y=280)
            fenster.update()
            with open(link, "r+") as f:
                for i, line in enumerate(f,1):
                    line = line.replace("\n", "")
                    if line == "":
                        continue
                    self.Links.append(line)
            for i,elem in enumerate(self.Links):
                elem = elem.strip()
                pb["value"] = 100 * (i /len(self.Links))
                fenster.update()
                try:
                    youtubeObject = YouTube(elem)
                    title = youtubeObject.title
                    title = title.replace("|", "").strip()
                    self.titles.append(title)
                    self.Status.append("Wartet")
                except:
                    self.Fehler += link + "\n"
                    self.titles.append("Fehler")
                    self.Status.append("Video nicht verfügbar/nicht öffentlich")
        self.Download_Übersicht()

    def Seite_1(self):
        Start().clearFrame()
        Start().Menü()
        label = tk.Label(fenster,text="Video-Download",font= ("Arial",20,"bold"))
        label2 = tk.Label(fenster, text="Bitte Auflösung auswählen:", font=("Arial", 10))
        label3 = tk.Label(fenster, text="Bitte Dateiformat auswählen:", font=("Arial", 10))
        label4 = tk.Label(fenster,text="Bitte Zielordner auswählen:",font= ("Arial",10))
        label5 = tk.Label(fenster,text="Bitte Modus auswählen:",font= ("Arial",10))
        self.label6 = tk.Label(fenster, text="Bitte Link eingeben:",font= ("Arial",10))
        self.text = tk.StringVar(None)
        self.text.set(value="")
        self.text2 = tk.StringVar(None)
        self.text2.set(value="")
        eingabefeld = tk.Entry(fenster, textvariable=self.text)
        eingabefeld2 = tk.Entry(fenster, textvariable=self.text2)
        self.auswahl = tk.StringVar(None)
        self.auswahl2 = tk.StringVar(None)
        self.auswahl3 = tk.StringVar(None)
        self.auswahl.set(value="Video(mp4)")
        self.auswahl2.set(value="1080p")
        self.auswahl3.set(value="einzelnes Video herunterladen")
        box = ttk.Combobox(fenster, textvariable=self.auswahl)
        self.box2 = ttk.Combobox(fenster, textvariable=self.auswahl2)
        box3 = ttk.Combobox(fenster, textvariable=self.auswahl3)
        values = ["Video(mp4)","Audio(mp3)"]
        values2 = ["bestmögliche Auflösung", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p",
                  "niedrigste Auflösung"]
        values3 = ["einzelnes Video herunterladen","Playlist herunterladen","Videolinks aus Dokument importieren"]
        box['values'] = values
        box['state'] = 'readonly'
        self.box2['values'] = values2
        self.box2['state'] = 'readonly'
        box3['values'] = values3
        box3['state'] = 'readonly'
        self.button = tk.Button(fenster, text="Weiter", command=lambda: [
        self.check_entry(box.get(),self.box2.get(),eingabefeld.get(),box3.get(),eingabefeld2.get())])
        button1 = tk.Button(fenster, text='▽', command=lambda: self.select_file(2))
        self.button2 = tk.Button(fenster, text='▽',state="disabled", command=lambda: self.select_file())
        box.bind("<<ComboboxSelected>>", self.callback)
        box3.bind("<<ComboboxSelected>>", self.callback)
        label.place(x = 135,y = 5)
        label2.place(x=10, y=85)
        label3.place(x=10, y=50)
        label4.place(x = 10,y = 120)
        label5.place(x = 10,y = 175)
        self.label6.place(x = 10,y = 220)
        eingabefeld.place(x = 240,y = 120,width=210,height=25)
        eingabefeld2.place(x = 240,y = 220,width=210,height=25)
        self.button.place(x = 225,y = 285)
        button1.place(x = 450,y = 120)
        self.button2.place(x = 450,y = 220)
        box.place(x=240, y=50, width=230, height=25)
        self.box2.place(x = 240,y = 85,width=230,height=25)
        box3.place(x=240, y=175, width=230, height=25)

    def Download_Übersicht(self):
        Start().clearFrame()
        Start().Menü2()
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
        self.status_table = ttk.Treeview(fenster,columns=cols,show='headings')
        for i,(link,title,status) in enumerate(zip(self.Links, self.titles, self.Status),start=1):
            self.status_table.insert("", "end", values=("%d)"%i,link,title,status))
        for col in cols:
            self.status_table.column(col, stretch=False)
            if col == "Nr.":
                self.status_table.column(col, stretch=False,width = 25)
            self.status_table.heading(col,text=col,anchor=tk.W)
        scroll_bar = ttk.Scrollbar(fenster, command=self.status_table.yview)
        scroll_bar2 = ttk.Scrollbar(fenster, command=self.status_table.xview, orient= "horizontal")
        self.status_table['yscrollcommand'] = scroll_bar.set
        self.status_table['xscrollcommand'] = scroll_bar2.set
        self.pb = ttk.Progressbar(fenster,style="text.Horizontal.TProgressbar",length=300,value=0)
        self.pb2 = ttk.Progressbar(fenster, style="text2.Horizontal.TProgressbar", length=300, value=0)
        self.button = tk.Button(fenster, text="Weiter",state= "disabled",command=lambda :self.Weiter())
        self.button2 = tk.Button(fenster, text="Start",command=lambda :self.Start())
        self.button3 = tk.Button(fenster, text="Pause",command=lambda :self.Pause())
        self.button4 = tk.Button(fenster, text="<--Zurück",command=lambda :self.Seite_1())
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

    def Start(self):
        self.index = 0
        self.Fehler = ""
        self.button2.config(text="Überspringen",command=lambda :self.Überspringen())
        self.pause = False
        self.skipped = False
        t1 = threading.Thread(target=self.Loop_Start)
        t1.daemon = True
        t1.start()

    def Pause(self):
        self.pause = True
        self.button.config(state="normal")
        self.button3.config(state="disabled")

    def Weiter(self):
        self.button3.config(state="normal")
        self.button2.config(state="normal")
        self.button.config(state="disabled")
        self.pause = False
        self.Download_Manager()

    def Überspringen(self):
        self.skipped = True

    def Loop_Start(self):
        self.skipped = False
        self.button2.config(state="normal")
        self.button3.config(state="normal")
        if not self.pause and self.index != len(self.Links):
            for j in range(6):
                if self.skipped or self.pause:
                    self.status = "Übersprungen"
                    break
                self.counter.config(text="Überspringen? " + str(5 - j) + "s")
                fenster.update()
                time.sleep(1.0)
            self.counter.config(text="")
            self.button2.config(state="disabled")
            self.button3.config(state="disabled")
            fenster.update()
        if self.skipped:
            self.Loop_End()
        else:
            self.Download_Manager()

    def Download_Manager(self):
        if self.index == len(self.Links):
            path = self.destination + "/Fehlgeschlagene Downloads.txt"
            try:
                os.remove(path)
            except:
                None
            if self.Fehler != "":
                with open(path,"w+") as f:
                    f.write(self.Fehler)
            self.button.destroy()
            self.button2.config(text="Beenden", command=lambda: fenster.quit())
            self.button2.config(state="normal")
            self.button3.destroy()
            self.counter.destroy()
            return None
        if not self.pause:
            self.pb["value"] = 0
            self.pb_label.configure('text.Horizontal.TProgressbar', text="Video wird heruntergeladen: 0 %")
            if self.titles[self.index].strip() == "Fehler":
                self.status = "Fehler"
                return self.Loop_End()
            line = ("%d)"%(self.index+1),self.Links[self.index ],self.titles[self.index],"Lädt herunter")
            selected_item = self.status_table.get_children()[self.index]
            self.status_table.delete(selected_item)
            self.status_table.tag_configure("Download", background="#90EE90")
            self.status_table.insert("",self.index ,values= line,tags="Download")
            self.t2 = threading.Thread(target=self.Download, args=[self.Links[self.index]])
            self.t2.daemon = True
            self.t2.start()

    def Loop_End(self):
        line = ("%d)"%(self.index+1),self.Links[self.index],self.titles[self.index],self.status)
        tag1 = self.status_table.tag_configure("Abgeschlossen",background="#90EE90")              # -> hellgrün
        tag2 = self.status_table.tag_configure("Fehler",background="#FFCCCB")                     # -> hellrot
        tag3 = self.status_table.tag_configure("Übersprungen",background="#add8e6")               # -> hellblau
        selected_item = self.status_table.get_children()[self.index]
        self.status_table.delete(selected_item)
        if self.status == "Fehler":
            self.status_table.insert("", self.index, values=line, tags="Fehler")
        elif self.status == "Datei existiert bereits" or self.status == "Übersprungen":
            self.status_table.insert("", self.index, values=line, tags="Übersprungen")
        else:
            self.status_table.insert("", self.index, values=line, tags="Abgeschlossen")
        self.pb2["value"] = int(((self.index+1) / len(self.Links)) * 100)
        self.pb_label2.configure('text2.Horizontal.TProgressbar', text= str(int(((self.index+1)/len(self.Links))*100))+" %")
        self.pb["value"] = 100
        self.pb_label.configure('text.Horizontal.TProgressbar', text="Abgeschlossen")
        fenster.update()
        self.index += 1
        self.Loop_Start()

    def Download_Progress(self,chunk, file_handle, bytes_remaining):
        percent = int((100 * (self.file_size - bytes_remaining)) / self.file_size)
        self.pb["value"] = percent
        if not self.video_downloaded:
            self.pb_label.configure('text.Horizontal.TProgressbar',text="Video wird heruntergeladen: " + str(percent) + " %")
        if self.only_audio or self.video_downloaded:
            self.pb_label.configure('text.Horizontal.TProgressbar', text="Audio wird heruntergeladen: "+str(percent) + " %")
        if percent >= 99 and not self.only_audio:
            self.video_downloaded = True
            self.pb_label.configure('text.Horizontal.TProgressbar', text="Audio wird heruntergeladen: "+str(percent) + " %")
        fenster.update()

    def Download(self,link):
        self.video_downloaded = False
        output_path = self.destination
        youtubeObject = YouTube(link,on_progress_callback=self.Download_Progress)
        title = youtubeObject.title
        if youtubeObject.age_restricted:
            self.Fehler += link + "\n"
            self.status = "Video ist altersbeschränkt"
            return self.Loop_End()
        for i in ["/", ":", "*", "<", ">", "|", "?",'"',"\\"]:
            title = title.replace(i, "")
        title = title.strip()
        tmp_title = title
        for i in [",", "^", "'", ".","#","$","%","~"]:
            tmp_title = tmp_title.replace(i, "")
        if self.only_audio:
            video_exists = False
            if os.path.exists(output_path + "/" + title + ".mp3"):
                self.status = "Datei existiert bereits"
                return self.Loop_End()
            if os.path.exists(output_path + "/" + title + ".mp4"):
                os.rename("%s/%s.mp4" % (output_path, title), "%s/tmp_video.mp4" % output_path)
                video_exists = True
            try:
                audio = youtubeObject.streams.filter(only_audio=True).first()
                self.file_size = audio.filesize
                audio.download("%s/" % output_path)
                os.rename("%s/%s.mp4" % (output_path, tmp_title), "%s/%s.mp3" % (output_path,title))
                if video_exists:
                    os.rename("%s/tmp_video.mp4" % output_path, "%s/%s.mp4" % (output_path, title))
                self.status = "Abgeschlossen"
                return self.Loop_End()
            except:
                if video_exists:
                    os.rename("%s/tmp_video.mp4" % output_path, "%s/%s.mp4" % (output_path, title))
                self.Fehler += link + "\n"
                self.status = "Fehler"
                return self.Loop_End()
        else:
            if os.path.exists(output_path + "/" + title + ".mp4"):
                self.status = "Datei existiert bereits"
                return self.Loop_End()
            if self.resolution == "bestmögliche Auflösung":
                video = youtubeObject.streams.get_highest_resolution()
            elif self.resolution == "niedrigste Auflösung":
                video = youtubeObject.streams.get_lowest_resolution()
            else:
                video = youtubeObject.streams.filter(res=self.resolution, file_extension="mp4").first()
            try:
                self.file_size = video.filesize
                video.download("%s" % output_path)
            except:
                video = youtubeObject.streams.get_highest_resolution()
                self.file_size = video.filesize
                video.download("%s" % output_path)
            try:
                audio = youtubeObject.streams.filter(only_audio=True).first()
                os.rename("%s/%s.mp4" % (output_path, tmp_title), "%s/tmp_video.mp4" % output_path)
                audio.download("%s/" % output_path)
                self.video_downloaded = False
                os.rename("%s/%s.mp4" % (output_path, tmp_title), "%s/tmp_audio.mp3" % output_path)
                mvp.ffmpeg_merge_video_audio("%s/tmp_video.mp4" % output_path, "%s/tmp_audio.mp3" % output_path,
                                             "%s/%s.mp4" % (output_path, title))
                os.remove("%s/tmp_video.mp4" % output_path)
                os.remove("%s/tmp_audio.mp3" % output_path)
                self.status = "Abgeschlossen"
                return self.Loop_End()
            except:
                try:
                    os.remove("%s/tmp_video.mp4" % output_path)
                    os.remove("%s/tmp_audio.mp3" % output_path)
                except:
                    None
                self.Fehler += link + "\n"
                self.status = "Fehler"
                return self.Loop_End()

if __name__ == "__main__":
    fenster = tk.Tk()
    fenster.title("Youtube_Download")
    fenster.geometry("500x350")
    fenster.resizable(False,False)
    Start().Seite_1()
    fenster.mainloop()